"""
github_push.py  —  Creates the GitHub repo and pushes all code.
No browser, no prompts, no gh CLI needed.

USAGE:
    1. Get a token:  https://github.com/settings/tokens/new
                     Check [x] repo  then Generate
    2. Run:  .\\venv\\Scripts\\python.exe github_push.py ghp_YOUR_TOKEN_HERE
"""
import sys, os, subprocess, json, urllib.request, urllib.error, base64

OWNER = "siddharth3105"
REPO  = "axis-ops-tracker"
PROJECT = os.path.dirname(os.path.abspath(__file__))
GIT = r"C:\Program Files\Git\bin\git.exe"

# ── helpers ──────────────────────────────────────────────────────

def gh_api(method, path, token, body=None):
    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization",  f"token {token}")
    req.add_header("Accept",         "application/vnd.github.v3+json")
    req.add_header("User-Agent",     "AxisOpsTracker/1.0")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r), r.status
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return json.loads(body) if body else {}, e.code

def git(*args):
    result = subprocess.run([GIT, "-C", PROJECT] + list(args),
                            capture_output=True, text=True)
    if result.returncode != 0 and result.stderr.strip():
        # print stderr but don't abort on push warnings
        print(f"   git stderr: {result.stderr.strip()[:200]}")
    return result.returncode, result.stdout.strip()

def step(n, msg):
    print(f"\n[{n}] {msg}")

# ── main ─────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 52)
    print("  Axis Ops Tracker  →  GitHub Push")
    print("=" * 52)

    # Get token
    if len(sys.argv) > 1:
        TOKEN = sys.argv[1].strip()
    else:
        print()
        TOKEN = input("  Paste your GitHub token (ghp_...): ").strip()

    if not TOKEN or TOKEN.startswith("YOUR_TOKEN"):
        print("\n  ERROR: No token provided.")
        print("  Get one at: https://github.com/settings/tokens/new")
        print("  Check [x] repo scope, then paste the ghp_... token here.")
        sys.exit(1)

    # Validate token
    step(1, "Validating token...")
    resp, code = gh_api("GET", "/user", TOKEN)
    if code != 200:
        print(f"   ERROR: Token invalid or expired (HTTP {code})")
        print("   Get a new one: https://github.com/settings/tokens/new")
        sys.exit(1)
    gh_user = resp.get("login", "unknown")
    print(f"   Authenticated as: {gh_user}")

    # Create repo
    step(2, f"Creating repo: {OWNER}/{REPO}...")
    resp, code = gh_api("GET", f"/repos/{OWNER}/{REPO}", TOKEN)
    if code == 200:
        print(f"   Repo already exists — skipping create.")
        clone_url = resp["clone_url"]
    else:
        body = {
            "name": REPO,
            "description": "Axis Ops employee tracker: Flask + SQLite + Google Sheets",
            "private": False,
            "auto_init": False
        }
        resp, code = gh_api("POST", "/user/repos", TOKEN, body)
        if code not in (200, 201):
            print(f"   ERROR creating repo: {resp}")
            sys.exit(1)
        clone_url = resp["clone_url"]
        print(f"   Created: {resp['html_url']}")

    # Configure git remote with token embedded
    step(3, "Configuring git remote...")
    auth_url = f"https://{gh_user}:{TOKEN}@github.com/{OWNER}/{REPO}.git"
    git("remote", "set-url", "origin", auth_url)
    print("   Remote set.")

    # Push
    step(4, "Pushing to GitHub...")
    code, out = git("push", "-u", "origin", "master")
    if code == 0:
        # Remove token from remote URL (security hygiene)
        git("remote", "set-url", "origin",
            f"https://github.com/{OWNER}/{REPO}.git")
        print()
        print("=" * 52)
        print("  SUCCESS! Repo is live:")
        print(f"  https://github.com/{OWNER}/{REPO}")
        print("=" * 52)
    else:
        print(f"   Push failed (exit {code})")
        # Try force push in case of history conflict
        print("   Trying with --force...")
        code2, _ = git("push", "-u", "origin", "master", "--force")
        if code2 == 0:
            git("remote", "set-url", "origin",
                f"https://github.com/{OWNER}/{REPO}.git")
            print()
            print("=" * 52)
            print("  SUCCESS (force push)! Repo is live:")
            print(f"  https://github.com/{OWNER}/{REPO}")
            print("=" * 52)
        else:
            print("   Force push also failed. Check token scope.")
            sys.exit(1)

if __name__ == "__main__":
    main()
