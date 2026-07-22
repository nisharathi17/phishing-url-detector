import re
from urllib.parse import urlparse


def extract_features(url):
    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "bank",
        "signin"
    ]

    # Parse URL
    parsed = urlparse(url)

    # Extract domain (works whether protocol exists or not)
    domain = parsed.netloc if parsed.netloc else parsed.path.split("/")[0]

    # Basic counts
    url_length = len(url)
    dot_count = url.count(".")
    hyphen_count = url.count("-")
    digit_count = sum(c.isdigit() for c in url)

    slash_count = url.count("/")
    question_count = url.count("?")
    equals_count = url.count("=")
    at_count = url.count("@")
    underscore_count = url.count("_")

    # Ratios
    digit_ratio = digit_count / max(url_length, 1)

    special_chars = sum(not c.isalnum() for c in url)
    special_char_ratio = special_chars / max(url_length, 1)

    # Suspicious keywords
    suspicious_word_count = sum(
        word in url.lower()
        for word in suspicious_words
    )

    # Domain features
    num_subdomains = max(0, domain.count(".") - 1)

    has_protocol = int(
        url.startswith("http://") or
        url.startswith("https://")
    )

    uses_https = int(
        url.startswith("https://")
    )

    # IP address detection
    has_ip_address = int(
        bool(
            re.search(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
                url
            )
        )
    )

    # Token-based feature
    tokens = re.split(r"[./?=&_-]", url)

    longest_token_length = max(
        (len(token) for token in tokens),
        default=0
    )

    return {
        "url_length": url_length,
        "url_count_dots": dot_count,
        "url_count_hyphens": hyphen_count,
        "has_protocol": has_protocol,
        "uses_https": uses_https,
        "digits": digit_count,
        "digit_ratio": digit_ratio,
        "num_slashes": slash_count,
        "num_question_marks": question_count,
        "num_equals": equals_count,
        "num_at_symbols": at_count,
        "num_underscores": underscore_count,
        "special_char_ratio": special_char_ratio,
        "suspicious_word_count": suspicious_word_count,
        "num_subdomains": num_subdomains,
        "has_ip_address": has_ip_address,
        "longest_token_length": longest_token_length
    }


if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://192.168.1.10/login",
        "http://paypal-login-secure-update.xyz"
    ]

    for url in test_urls:
        print("=" * 50)
        print(url)
        print(extract_features(url))