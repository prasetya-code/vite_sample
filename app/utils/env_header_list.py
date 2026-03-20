# List Header
STANDARD_HEADERS = {
    # ================= SECURITY =================
    "security": [
        "Strict-Transport-Security",  
        # contoh: max-age=63072000; includeSubDomains; preload

        "Content-Security-Policy",  
        # contoh: default-src 'self'; script-src 'self' https://cdn.example.com; object-src 'none'; base-uri 'self'

        "Content-Security-Policy-Report-Only",  
        # contoh: default-src 'self'; report-uri https://report.example.com/csp

        "X-Frame-Options",  
        # contoh: DENY  |  SAMEORIGIN

        "X-Content-Type-Options",  
        # contoh: nosniff

        "Referrer-Policy",  
        # contoh: strict-origin-when-cross-origin

        "Permissions-Policy",  
        # contoh: geolocation=(), microphone=(), camera=()

        "Clear-Site-Data",  
        # contoh: "cache", "cookies", "storage", "executionContexts"

        "Origin-Agent-Cluster",  
        # contoh: ?1

        "Timing-Allow-Origin",  
        # contoh: https://app.example.com

        "X-XSS-Protection",  
        # contoh: 1; mode=block   (legacy)

        "X-Permitted-Cross-Domain-Policies",  
        # contoh: none

        "Expect-CT",  
        # contoh: max-age=86400, enforce, report-uri="https://report.example.com/ct"

        "Report-To",  
        # contoh: {"group":"default","max_age":10886400,"endpoints":[{"url":"https://report.example.com"}]}

        "NEL",  
        # contoh: {"report_to":"default","max_age":10886400,"include_subdomains":true}

        # Cross Origin Isolation
        "Cross-Origin-Opener-Policy",  
        # contoh: same-origin

        "Cross-Origin-Embedder-Policy",  
        # contoh: require-corp

        "Cross-Origin-Resource-Policy"  
        # contoh: same-origin
    ],

    # ================= CORS =================
    "cors": [
        "Origin",  
        # contoh: https://app.example.com

        "Vary",  
        # contoh: Origin, Access-Control-Request-Method, Access-Control-Request-Headers

        "Access-Control-Allow-Origin",  
        # contoh: https://app.example.com   |  *   (jangan pakai * jika Allow-Credentials true)

        "Access-Control-Allow-Methods",  
        # contoh: GET, POST, PUT, DELETE, OPTIONS

        "Access-Control-Allow-Headers",  
        # contoh: Authorization, Content-Type, X-Requested-With

        "Access-Control-Allow-Credentials",  
        # contoh: true

        "Access-Control-Expose-Headers",  
        # contoh: Content-Length, X-Request-Id

        "Access-Control-Max-Age",  
        # contoh: 86400

        "Access-Control-Request-Method",  
        # contoh: POST

        "Access-Control-Request-Headers"  
        # contoh: Authorization, Content-Type
    ],

    # ================= PRIVACY / AUTH =================
    "privacy": [
        "Authorization",  
        # contoh: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

        "Proxy-Authenticate",  
        # contoh: Basic realm="Proxy Area"

        "WWW-Authenticate",  
        # contoh: Bearer realm="api", error="invalid_token"

        "Authentication-Info",  
        # contoh: nextnonce="xyz", qop="auth"

        "Set-Cookie",  
        # contoh: sessionid=abc123; HttpOnly; Secure; SameSite=Strict; Path=/

        "Cookie",  
        # contoh: sessionid=abc123; theme=dark

        "X-CSRF-Token",  
        # contoh: 4f3c2a1b9d...

        "X-API-Key",  
        # contoh: sk_live_abc123xyz

        "Sec-Fetch-Site",  
        # contoh: same-origin | same-site | cross-site | none

        "Sec-Fetch-Mode",  
        # contoh: navigate | cors | no-cors | same-origin

        "Sec-Fetch-User",  
        # contoh: ?1

        "Sec-Fetch-Dest"  
        # contoh: document | image | script | style | empty
    ],

    # ================= CACHING =================
    "caching": [
        "Cache-Control",  
        # contoh: public, max-age=3600, s-maxage=86400, immutable

        "Pragma",  
        # contoh: no-cache

        "Expires",  
        # contoh: Wed, 21 Oct 2026 07:28:00 GMT

        "ETag",  
        # contoh: "686897696a7c876b7e"

        "Last-Modified",  
        # contoh: Tue, 20 Oct 2026 07:28:00 GMT

        "If-None-Match",  
        # contoh: "686897696a7c876b7e"

        "If-Modified-Since",  
        # contoh: Tue, 20 Oct 2026 07:28:00 GMT

        "Age",  
        # contoh: 5400

        "Warning",  
        # contoh: 110 - "Response is stale"

        "Surrogate-Control",  
        # contoh: max-age=86400

        "CDN-Cache-Control"  
        # contoh: max-age=31536000, public
    ],

    # ================= CONTENT =================
    "content": [
        "Content-Type",  
        # contoh: text/html; charset=utf-8  |  application/json

        "Content-Length",  
        # contoh: 3487

        "Content-Encoding",  
        # contoh: gzip  |  br  |  zstd

        "Content-Disposition",  
        # contoh: inline  |  attachment; filename="report.pdf"

        "Content-Language",  
        # contoh: en-US  |  id-ID

        "Accept",  
        # contoh: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

        "Accept-Encoding",  
        # contoh: gzip, deflate, br, zstd

        "Accept-Language",  
        # contoh: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7

        "Accept-Charset",  
        # contoh: utf-8

        "Accept-Ranges",  
        # contoh: bytes

        "Range",  
        # contoh: bytes=0-1023

        "User-Agent"  
        # contoh: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0 Safari/537.36
    ],

    # ================= TRANSPORT =================
    "transport": [
        "Host",  
        # contoh: api.example.com

        "Connection",  
        # contoh: keep-alive  |  close

        "Upgrade-Insecure-Requests",  
        # contoh: 1

        "Transfer-Encoding",  
        # contoh: chunked

        "TE",  
        # contoh: trailers

        "Trailer",  
        # contoh: Expires, Content-MD5

        "Via",  
        # contoh: 1.1 varnish, 1.1 nginx

        "Forwarded",  
        # contoh: for=203.0.113.43;proto=https;host=api.example.com

        "X-Forwarded-For",  
        # contoh: 203.0.113.43

        "X-Forwarded-Proto",  
        # contoh: https

        "Alt-Svc",  
        # contoh: h3=":443"; ma=86400

        "Early-Data",  
        # contoh: 1

        "Keep-Alive"  
        # contoh: timeout=5, max=100
    ],

    # ================= PROTOCOL / INFRA =================
    "protocol": [
        "Server",  
        # contoh: nginx/1.26.0

        "Date",  
        # contoh: Wed, 21 Oct 2026 07:28:00 GMT

        "Allow",  
        # contoh: GET, POST, PUT, DELETE, OPTIONS

        "Location",  
        # contoh: https://api.example.com/v2/resource

        "Retry-After",  
        # contoh: 120   |   Wed, 21 Oct 2026 07:30:00 GMT

        "Link",  
        # contoh: <https://api.example.com/page/2>; rel="next"

        "Accept-Patch",  
        # contoh: application/json-patch+json

        "Accept-Post",  
        # contoh: application/json

        "Prefer",  
        # contoh: return=minimal, wait=10

        "Preference-Applied",  
        # contoh: return=minimal

        "Upgrade"  
        # contoh: h2c
    ],

    # ================= OBSERVABILITY =================
    "observability": [
        "Traceparent",  
        # contoh: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01

        "Tracestate",  
        # contoh: rojo=00f067aa0ba902b7,congo=t61rcWkgMzE

        "X-Request-Id",  
        # contoh: 550e8400-e29b-41d4-a716-446655440000

        "X-Correlation-Id",  
        # contoh: order-service-123456

        "X-B3-TraceId",  
        # contoh: 80f198ee56343ba864fe8b2a57d3eff7

        "X-B3-SpanId",  
        # contoh: e457b5a2e4d86bd1

        "X-B3-Sampled",  
        # contoh: 1

        "X-B3-Flags"  
        # contoh: 1
    ],

    # ================= DEBUG / LEGACY =================
    "legacy": [
        "DNT",  
        # contoh: 1

        "Public-Key-Pins",  
        # contoh: pin-sha256="base64=="; max-age=5184000; includeSubDomains
        # (deprecated — jangan dipakai di produksi)

        "Public-Key-Pins-Report-Only",  
        # contoh: pin-sha256="base64=="; max-age=5184000; report-uri="https://report.example.com"
        # (deprecated)

        "X-Powered-By",  
        # contoh: PHP/8.3.1   |  Express

        "X-AspNet-Version",  
        # contoh: 4.0.30319

        "X-AspNetMvc-Version"  
        # contoh: 5.2
    ]


}