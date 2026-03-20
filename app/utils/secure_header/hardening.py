def extra_hardening(response):

    response.headers["Expect-CT"] = "max-age=86400, enforce"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

    return response


def header_hiding(response):

    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)
    response.headers.pop("Via", None)
    response.headers.pop("ETag", None)
    response.headers.pop("Last-Modified", None)

    response.headers["Server"] = "secure"

    return response


def paranoid_headers(response):

    response.headers["Accept-CH"] = ""
    response.headers["Accept-CH-Lifetime"] = "0"
    response.headers["Timing-Allow-Origin"] = "none"
    response.headers["X-Download-Options"] = "noopen"
    response.headers["Vary"] = "Accept-Encoding"

    return response