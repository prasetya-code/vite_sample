def cache(response):

    if response.mimetype == "application/json":
        response.headers["Cache-Control"] = "no-store"
    else:
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

    return response