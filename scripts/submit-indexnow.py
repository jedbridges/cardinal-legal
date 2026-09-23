"""Tell Bing, Yandex, Seznam and Naver that this site's pages exist.

IndexNow needs no account and no verification: the key below is proved by
serving it at the site root, which is what 267de0147f1d471bb1998f9a47dcf79f.txt
is for. Google does not participate, so Google still needs Search Console.

    python3 scripts/submit-indexnow.py            # every URL in sitemap.xml
    python3 scripts/submit-indexnow.py /quiet-time/   # just these

Run it after publishing a new page or materially rewriting one. Submitting
unchanged URLs repeatedly is the one thing the protocol asks you not to do,
so this is not a cron job.
"""

import json, pathlib, re, sys, urllib.request

KEY = "267de0147f1d471bb1998f9a47dcf79f"
HOST = "cardinalbible.app"
ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.indexnow.org/IndexNow"


def from_sitemap():
    xml = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)


def main():
    args = sys.argv[1:]
    urls = [f"https://{HOST}{a}" if a.startswith("/") else a for a in args] or from_sitemap()

    # The key file must be live, or every submission is rejected as unverified.
    probe = f"https://{HOST}/{KEY}.txt"
    try:
        served = urllib.request.urlopen(probe, timeout=15).read().decode().strip()
    except Exception as e:
        sys.exit(f"key file unreachable at {probe}: {e}\nPush it before submitting.")
    if served != KEY:
        sys.exit(f"key file at {probe} holds {served!r}, expected {KEY!r}")

    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": probe, "urlList": urls})
    req = urllib.request.Request(
        ENDPOINT, data=body.encode(), headers={"Content-Type": "application/json; charset=utf-8"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code

    # 200 accepted, 202 accepted but key still being validated. Both are fine.
    if code not in (200, 202):
        sys.exit(f"IndexNow returned {code} for {len(urls)} URLs")
    print(f"submitted {len(urls)} URLs, HTTP {code}")
    for u in urls:
        print(f"  {u}")


if __name__ == "__main__":
    main()
