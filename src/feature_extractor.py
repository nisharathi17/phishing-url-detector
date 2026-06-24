from PIL.features import features
from tornado.web import url


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
    return {
        "url_length": len(url),
        "url_count_dots": url.count("."),
        "url_count_hyphens": url.count("-"),
        "starts_with_http": int(url.startswith("http")),
        "digits": sum(c.isdigit() for c in url),
        "num_slashes": url.count("/"),
        "num_question_marks": url.count("?"),
        "num_equals": url.count("="),
        "num_at_symbols": url.count("@"),
        "num_underscores": url.count("_"),
        "suspicious_word_count": sum(
    word in url.lower()
    for word in suspicious_words
      )
    }
if __name__ == "__main__":
    print(extract_features("http://google123.com"))

