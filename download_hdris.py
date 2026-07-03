#!/usr/bin/env python3
"""Download CC0 HDRIs from ambientCG API for environment lighting."""
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hdris")
os.makedirs(OUTDIR, exist_ok=True)

API_BASE = "https://ambientcg.com/api/v2"

def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
    return None

def download_file(url, outpath, timeout=120):
    try:
        result = subprocess.run(
            ["curl", "-sL", "-o", outpath, url, "-w", "%{http_code}:%{size_download}"],
            capture_output=True, text=True, timeout=timeout
        )
        code, size = result.stdout.strip().split(":")
        return int(code), int(size)
    except Exception as e:
        return 0, str(e)

# Define which HDRI types to get
categories = [
    "DaySkyHDRI",
    "DayEnvironmentHDRI", 
    "EveningSkyHDRI",
    "NightSkyHDRI",
    "NightEnvironmentHDRI",
    "StudioHDRI",
]

# Target: 4-6 good HDRIs covering different lighting scenarios
# Get 2 from each of the most useful categories
target_categories = {
    "DayEnvironmentHDRI": 1,   # Outdoor daytime
    "EveningSkyHDRI": 1,       # Sunset/golden hour
    "NightSkyHDRI": 1,         # Nighttime
    "StudioHDRI": 1,           # Studio/interior
    "DaySkyHDRI": 1,           # Open sky
}

downloaded = []

for cat, needed in target_categories.items():
    if needed <= 0:
        continue
    print(f"\n--- {cat} (need {needed}) ---")
    url = f"{API_BASE}/full_json?type=HDRI&categories={cat}&limit={needed+1}&include=downloadData,fileData&sort=downloads"
    data = fetch_json(url)
    if not data or not data.get("foundAssets"):
        print(f"  No assets found for {cat}")
        continue
    
    for asset in data["foundAssets"][:needed]:
        asset_id = asset.get("assetId", "")
        name = asset.get("displayName", asset_id)
        dl_folders = asset.get("downloadFolders", {})
        if not dl_folders:
            print(f"  {name}: no download folders")
            continue
        
        # Get 2K download URL
        dl_url = None
        default = dl_folders.get("default", {})
        if default:
            cats = default.get("downloadFiletypeCategories", {})
            for fmt in ["zip"]:
                if fmt in cats:
                    for dl in cats[fmt].get("downloads", []):
                        if dl.get("attribute") == "2K":
                            dl_url = dl.get("fullDownloadPath") or dl.get("downloadLink")
                            break
                    if dl_url:
                        break
        
        if not dl_url:
            # Try direct pattern
            dl_url = f"https://ambientcg.com/get?file={asset_id}_2K.zip"
        
        outpath = os.path.join(OUTDIR, f"{asset_id}_2K.zip")
        if os.path.exists(outpath):
            print(f"  {name}: already exists")
            downloaded.append(asset_id)
            continue
        
        print(f"  Downloading {name} (2K)...")
        code, size = download_file(dl_url, outpath)
        if code == 200:
            print(f"    HTTP 200, {size} bytes")
            downloaded.append(asset_id)
        else:
            print(f"    HTTP {code}")
            # Clean up failed download
            if os.path.exists(outpath) and os.path.getsize(outpath) < 100:
                os.remove(outpath)

print(f"\n{'='*50}")
print(f"Downloaded {len(downloaded)} HDRIs to {OUTDIR}")
for h in downloaded:
    print(f"  - {h}")
