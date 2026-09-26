import base64, hashlib, hmac, json, time
from .config import settings

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), settings.secret_key.encode(), 210_000).hex()

def verify_password(password: str, digest: str) -> bool:
    return hmac.compare_digest(hash_password(password), digest)

def create_token(email: str, role: str, ttl: int = 86400) -> str:
    payload={"sub":email,"role":role,"exp":int(time.time())+ttl}
    raw=base64.urlsafe_b64encode(json.dumps(payload,separators=(",",":")).encode()).decode().rstrip("=")
    sig=hmac.new(settings.secret_key.encode(), raw.encode(), hashlib.sha256).hexdigest()
    return raw+"."+sig

def decode_token(token: str):
    raw,sig=token.split(".",1)
    expected=hmac.new(settings.secret_key.encode(), raw.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected): raise ValueError("invalid token")
    payload=json.loads(base64.urlsafe_b64decode(raw+"==="))
    if payload["exp"] < int(time.time()): raise ValueError("expired token")
    return payload
