from flask import g, request
import secrets

def generate_nonce():
    return secrets.token_urlsafe(16)

def attach_nonce():
    """
    Before-request hook untuk generate CSP nonce per request.
    Hanya untuk non-API.
    """
    if not request.path.startswith("/api"):
        g.csp_nonce = generate_nonce()

# Ambil value objek dari csp_nonce 
def get_nonce():
    return getattr(g, "csp_nonce", None)