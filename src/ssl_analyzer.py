import socket
import ssl
from datetime import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID, NameOID


KNOWN_CAS = (
    "digicert", "let's encrypt", "sectigo", "godaddy", "globalsign",
    "comodo", "amazon", "google trust services", "microsoft", "entrust",
    "identrust", "cloudflare", "ssl.com", "buypass",
)


def _get_certificate(hostname, port=443, timeout=5):
    """
    Open a TLS connection and pull the raw certificate WITHOUT validating it.

    We deliberately skip verification (CERT_NONE) so we can inspect certs on
    sites with invalid, self-signed, expired, or mismatched certs -- that's
    exactly the signal we're trying to capture for phishing detection.
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            der = ssock.getpeercert(binary_form=True)

    return x509.load_der_x509_certificate(der, default_backend())


def _check_hostname(hostname, cert):
    """Return (matches: bool, san_count: int) for the given hostname vs cert."""
    hostname = hostname.lower()
    names = set()

    try:
        cn = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cn:
            names.add(cn[0].value.lower())
    except Exception:
        pass

    san_count = 0
    try:
        san_ext = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
        san_names = san_ext.value.get_values_for_type(x509.DNSName)
        san_count = len(san_names)
        names.update(n.lower() for n in san_names)
    except x509.ExtensionNotFound:
        pass

    matches = False
    for name in names:
        if name == hostname:
            matches = True
            break
        if name.startswith("*.") and hostname.endswith(name[1:]):
            matches = True
            break

    return matches, san_count


def analyze_ssl(domain, port=443, timeout=5):
    """
    Analyze the TLS certificate served by `domain`.

    If the connection/handshake fails (no HTTPS, timeout, refused, etc.),
    returns a "no cert" feature set instead of raising -- a missing or
    broken cert is itself a strong phishing signal, not an error to hide.
    """
    no_cert_result = {
        "ssl_has_cert": 0,
        "ssl_valid_window": 0,
        "ssl_self_signed": 0,
        "ssl_hostname_mismatch": 1,
        "ssl_days_to_expiry": -1,
        "ssl_cert_age_days": -1,
        "ssl_validity_period_days": -1,
        "ssl_san_count": 0,
        "ssl_issuer_known_ca": 0,
    }

    try:
        cert = _get_certificate(domain, port=port, timeout=timeout)
    except Exception:
        return no_cert_result

    now = datetime.utcnow()
    not_before = cert.not_valid_before
    not_after = cert.not_valid_after

    days_to_expiry = (not_after - now).days
    cert_age_days = (now - not_before).days
    validity_period_days = (not_after - not_before).days
    valid_window = int(not_before <= now <= not_after)

    self_signed = int(cert.issuer == cert.subject)

    hostname_matches, san_count = _check_hostname(domain, cert)

    issuer_cn = ""
    try:
        cn = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cn:
            issuer_cn = cn[0].value.lower()
    except Exception:
        pass
    issuer_known_ca = int(any(ca in issuer_cn for ca in KNOWN_CAS))

    return {
        "ssl_has_cert": 1,
        "ssl_valid_window": valid_window,
        "ssl_self_signed": self_signed,
        "ssl_hostname_mismatch": int(not hostname_matches),
        "ssl_days_to_expiry": days_to_expiry,
        "ssl_cert_age_days": cert_age_days,
        "ssl_validity_period_days": validity_period_days,
        "ssl_san_count": san_count,
        "ssl_issuer_known_ca": issuer_known_ca,
    }


if __name__ == "__main__":
    test_domains = [
        "www.google.com",
        "expired.badssl.com",
        "self-signed.badssl.com",
        "wrong.host.badssl.com",
    ]

    for d in test_domains:
        print("=" * 50)
        print(d)
        print(analyze_ssl(d))