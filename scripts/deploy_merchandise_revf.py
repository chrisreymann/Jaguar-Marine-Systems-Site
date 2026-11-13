#!/usr/bin/env python3
"""Deploy the exact, user-approved Rev F merchandise preview package.
Runs in GitHub Actions only after a ZIP is uploaded to incoming/.
"""
from pathlib import Path
import hashlib
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "incoming" / "JMS_Merchandise_RevF_Publish_Package.zip"
EXPECTED_SHA256 = "9106c7bf47842978de49e0ec7d88a647dc4124bd8802b04b62f0b4dc5fd82d67"
FILES = [
    "merchandise.html",
    "assets/merchandise/ocean-guardian-001-approved.webp",
    "assets/merchandise/jms-hex-reef-approved.webp",
    "assets/merchandise/balam-ha-institute-approved.webp",
    "assets/merchandise/mangrove-coral-approved.webp",
    "assets/merchandise/approved-storefront-composite.png",
    "assets/merchandise/approved-design-sheet.png",
]
if not ZIP.is_file():
    print("No incoming Rev F ZIP; nothing to deploy.")
    sys.exit(0)
digest = hashlib.sha256(ZIP.read_bytes()).hexdigest()
if digest != EXPECTED_SHA256:
    raise SystemExit("Rev F ZIP hash mismatch: refusing to deploy altered or incorrect artwork.")
with zipfile.ZipFile(ZIP) as archive:
    names = set(archive.namelist())
    missing = set(FILES) - names
    if missing:
        raise SystemExit("ZIP missing required files: " + ", ".join(sorted(missing)))
    html = archive.read("merchandise.html").decode("utf-8")
    if not all(name in html for name in FILES[1:6]):
        raise SystemExit("HTML does not reference the required approved artwork paths.")
    if "print file" not in html.lower():
        raise SystemExit("Missing print-quality disclaimer.")
    for name in FILES:
        data = archive.read(name)
        if not data or len(data) > 5_000_000:
            raise SystemExit("Invalid or oversized asset: " + name)
        dest = ROOT / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True, cwd=ROOT)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True, cwd=ROOT)
subprocess.run(["git", "add", "--", *FILES], check=True, cwd=ROOT)
subprocess.run(["git", "rm", "-f", "--", str(ZIP.relative_to(ROOT))], check=True, cwd=ROOT)
diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
if diff.returncode == 0:
    print("No changes to commit.")
else:
    subprocess.run(["git", "commit", "-m", "Publish approved Rev F Ocean Guardians storefront previews"], check=True, cwd=ROOT)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True, cwd=ROOT)
print("Rev F approved preview assets deployed; print production remains pending.")
