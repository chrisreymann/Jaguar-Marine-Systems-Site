#!/usr/bin/env python3
"""Publish the exact approved Rev F merchandise ZIP regardless of download filename."""
from pathlib import Path
import hashlib
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
INCOMING = ROOT / "incoming"
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
candidates = sorted(INCOMING.glob("*.zip"))
matches = [p for p in candidates if hashlib.sha256(p.read_bytes()).hexdigest() == EXPECTED_SHA256]
if not matches:
    raise SystemExit("No matching approved Rev F ZIP in incoming/. Keep unrecognized uploads unchanged.")
source = matches[0]
print(f"Verified approved Rev F archive: {source.name}")
with zipfile.ZipFile(source) as archive:
    names = set(archive.namelist())
    missing = set(FILES) - names
    if missing:
        raise SystemExit("ZIP missing required files: " + ", ".join(sorted(missing)))
    html = archive.read("merchandise.html").decode("utf-8")
    if not all(name in html for name in FILES[1:6]):
        raise SystemExit("HTML does not reference approved artwork paths.")
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
subprocess.run(["git", "rm", "-f", "--", *[str(p.relative_to(ROOT)) for p in matches]], check=True, cwd=ROOT)
diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
if diff.returncode == 0:
    print("No changes to commit.")
else:
    subprocess.run(["git", "commit", "-m", "Publish approved Rev F Ocean Guardians storefront previews"], check=True, cwd=ROOT)
    subprocess.run(["git", "push", "origin", "HEAD:main"], check=True, cwd=ROOT)
print("Approved Rev F previews deployed; these are not print-ready masters.")
