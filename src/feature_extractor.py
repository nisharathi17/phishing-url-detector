def extract_features(url):

    return {
        "url_length": len(url),
        "url_count_dots": url.count("."),
        "url_count_hyphens": url.count("-"),
        "starts_with_http": int(url.startswith("http")),
        "digits": sum(c.isdigit() for c in url)
    }
if __name__ == "__main__":
    print(extract_features("http://google123.com"))

