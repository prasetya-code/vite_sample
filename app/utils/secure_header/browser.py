def browser_privacy(response):

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"

    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    response.headers["Permissions-Policy"] = (
        "geolocation=(), microphone=(), camera=(), usb=(), bluetooth=(), "
        "interest-cohort=(), browsing-topics=()"
    )

    return response