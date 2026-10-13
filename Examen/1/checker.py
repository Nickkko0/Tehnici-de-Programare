import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    host = host.rstrip("/")
    path = path.lstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "https://" + host
    return (host + "/" + path)
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url, timeout=10)
    content_type = r.headers.get("Content-Type")
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {content_type}")
    print(r, h)
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=10)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type"),
            "length": len(r.content),
            "server": r.headers.get("Server"),
        }
    except requests.RequestException:
        return {"status": None, "content_type": None, "length": 0, "server": None}
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    ok = 0
    for url in SITES:
        info = check_site(url)
        if info["status"] is not None and info["status"] < 400:
            ok += 1
            print(f"[OK] {url} -> {info['status']} ({info['length']} bytes)")
    print(f"Rezumat: {ok}/{len(SITES)} site-uri funcționează")
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        headers = requests.get(url, timeout=10).headers
    except requests.RequestException:
        return {"present": [], "missing": SECURITY_HEADERS[:], "score": 0}
    present = [h for h in SECURITY_HEADERS if h in headers]
    missing = [h for h in SECURITY_HEADERS if h not in headers]
    score = round(len(present) / len(SECURITY_HEADERS) * 100)
    return {"present": present, "missing": missing, "score": score}
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    for i in range(1, attempts + 1):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code < 500:
                return {"status": r.status_code, "attempts": i}
        except requests.RequestException:
            pass
    return {"status": None, "attempts": attempts}
    pass
