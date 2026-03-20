import os

# =====================================================
# CSP KEYWORDS (agar tidak mengulang string)
# =====================================================

SELF = "'self'"
NONE = "'none'"
UNSAFE_EVAL = "'unsafe-eval'"


def csp_policy(nonce=None, mode="web"):
    """
    mode:
        web -> website normal
        spa -> frontend SPA
        api -> API backend
    """

    # =====================================================
    # SCRIPT SOURCE
    # =====================================================
    script_src = [
        SELF,  # hanya script dari domain sendiri

        UNSAFE_EVAL,  # dibutuhkan oleh beberapa framework JS (React dev, bundler tertentu)

        # ICONIFY CDN
        "https://code.iconify.design",

        # LOTTIE CDN
        "https://unpkg.com",            # CDN untuk paket JS (termasuk lottie-web)
        "https://cdnjs.cloudflare.com", # CDN umum (Cloudflare CDN)
    ]

    # =====================================================
    # STYLE SOURCE
    # =====================================================
    style_src = [
        SELF,

        # GOOGLE FONTS STYLESHEET
        "https://fonts.googleapis.com",
    ]

    # =====================================================
    # FONT SOURCE
    # =====================================================
    font_src = [
        SELF,

        # GOOGLE FONTS FILE HOST
        "https://fonts.gstatic.com",
    ]

    # =====================================================
    # CONNECT SOURCE (AJAX / API / FETCH)
    # =====================================================
    connect_src = [
        SELF,

        # ICONIFY API
        "https://api.iconify.design",
        "https://api.simplesvg.com",
        "https://api.unisvg.com",

        # LOTTIE FILE HOST
        "https://assets.lottiefiles.com",
        "https://lottie.host",
    ]

    # =====================================================
    # IMAGE SOURCE
    # =====================================================
    img_src = [
        SELF,

        "data:",  # memungkinkan base64 image

        # LOTTIE IMAGE ASSET
        "https://assets.lottiefiles.com",
        "https://lottie.host",
    ]

    # =====================================================
    # NONCE (untuk inline script/style yang aman)
    # =====================================================
    if nonce:
        script_src.append(f"'nonce-{nonce}'")
        style_src.append(f"'nonce-{nonce}'")

    # =====================================================
    # MODE SPA
    # =====================================================
    if mode == "spa":
        # endpoint API frontend
        connect_src.append("https://api.yourdomain.com")

    # =====================================================
    # CSP POLICY BUILD
    # =====================================================
    return (
        f"default-src {NONE}; "

        # paksa HTTPS
        "upgrade-insecure-requests; "

        # blok mixed content
        "block-all-mixed-content; "

        f"script-src {' '.join(script_src)}; "
        f"script-src-elem {' '.join(script_src)}; "

        f"style-src {' '.join(style_src)}; "
        f"style-src-elem {' '.join(style_src)}; "

        f"font-src {' '.join(font_src)}; "

        f"img-src {' '.join(img_src)}; "

        f"connect-src {' '.join(connect_src)}; "

        # blok plugin lama
        f"object-src {NONE}; "

        # blok embedding website ke iframe
        f"frame-ancestors {NONE}; "

        # batasi base tag
        f"base-uri {NONE}; "

        # hanya boleh submit form ke domain sendiri
        f"form-action {SELF}; "

        # manifest PWA
        f"manifest-src {SELF}; "

        # web worker
        f"worker-src {SELF}; "

        # media source
        f"media-src {SELF}; "

        # Trusted Types untuk mencegah DOM XSS
        "require-trusted-types-for 'script'; "
        "trusted-types default; "

        # CSP reporting
        "report-uri /csp-report; "
        "report-to csp-endpoint; "
    )


def csp_headers(response, nonce=None, mode="web"):
    """
    Menerapkan header CSP ke response.
    """

    if mode == "api":
        return response

    csp = csp_policy(nonce, mode)

    # mode report-only untuk debugging CSP
    if os.getenv("CSP_REPORT_ONLY", "false").lower() == "true":
        response.headers["Content-Security-Policy-Report-Only"] = csp

    else:
        response.headers["Content-Security-Policy"] = csp

    return response


def csp_report(response, mode="web"):
    """
    Header Report-To untuk CSP modern browser.
    Digunakan untuk menerima laporan pelanggaran CSP.
    """

    if mode == "api":
        return response

    response.headers["Report-To"] = (
        "{"
        '"group":"csp-endpoint",'
        '"max_age":10886400,'
        '"endpoints":[{"url":"/csp-report"}]'
        "}"
    )

    return response