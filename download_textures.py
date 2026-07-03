#!/usr/bin/env python3
"""Download top CC0 PBR textures from ambientCG for FPS game asset kit.

Queries the ambientCG API v2 for popular assets in each target category,
then downloads 2K JPG zip files (best quality-size tradeoff).
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import zipfile
import io

API_BASE = "https://ambientcg.com/api/v2"
TEXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "textures")
os.makedirs(TEXTURES_DIR, exist_ok=True)

# Target categories for an FPS game environment
TARGET_CATEGORIES = [
    "Concrete",
    "Metal",
    "Wood",
    "Bricks",
    "Ground",
    "Rock",
    "Plaster",
    "Asphalt",
    "Floor",
    "Wall",
]

# Number of top assets to fetch per category
ASSETS_PER_CATEGORY = 3

# Resolution to download (2K JPG = good quality, ~10MB per texture)
RESOLUTION = "2K-JPG"


def fetch_json(url):
    """Fetch and parse JSON from URL with retry."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fps-asset-kit/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            print(f"  Retry {attempt + 1}/3: {e}")
            time.sleep(2)
    return None


def get_assets_for_category(category, limit=3):
    """Get top assets for a category sorted by popularity."""
    url = (
        f"{API_BASE}/full_json"
        f"?category={category}"
        f"&type=Material"
        f"&sort=Popular"
        f"&limit={limit}"
        f"&include=downloadData"
    )
    print(f"  Querying: {category} (limit={limit})")
    data = fetch_json(url)
    if data and "foundAssets" in data:
        return data["foundAssets"]
    return []


def find_download(asset, resolution):
    """Find the download URL for a specific resolution."""
    folders = asset.get("downloadFolders", {})
    default = folders.get("default", {})
    filetype_cats = default.get("downloadFiletypeCategories", {})
    zip_cat = filetype_cats.get("zip", {})
    downloads = zip_cat.get("downloads", [])

    # Try to match the resolution string (e.g., "2K-JPG")
    for d in downloads:
        if d.get("attribute") == resolution:
            return d.get("fullDownloadPath")
    # Fallback: take the first JPG download
    for d in downloads:
        if "JPG" in d.get("attribute", ""):
            return d.get("fullDownloadPath")
    # Last resort: first available
    if downloads:
        return downloads[0].get("fullDownloadPath")
    return None


def download_file(url, dest_path):
    """Download a file, skipping if already exists."""
    if os.path.exists(dest_path):
        print(f"    Already exists, skipping: {dest_path}")
        return True
    print(f"    Downloading: {url}")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fps-asset-kit/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "wb") as f:
                f.write(data)
            size_mb = len(data) / (1024 * 1024)
            print(f"    Saved: {dest_path} ({size_mb:.1f} MB)")
            return True
        except Exception as e:
            print(f"    Attempt {attempt + 1}/3 failed: {e}")
            time.sleep(3)
    return False


def extract_zip_in_place(zip_path, extract_dir):
    """Extract a zip archive and remove the zip file afterwards."""
    if not os.path.exists(zip_path):
        return
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            os.makedirs(extract_dir, exist_ok=True)
            zf.extractall(extract_dir)
        os.remove(zip_path)
        print(f"    Extracted: {zip_path} -> {extract_dir}")
    except zipfile.BadZipFile:
        print(f"    Bad zip, keeping as-is: {zip_path}")


def main():
    print("=" * 60)
    print("FPS Asset Kit — ambientCG Texture Downloader")
    print("=" * 60)

    all_downloaded = 0
    all_skipped = 0
    all_failed = 0

    for category in TARGET_CATEGORIES:
        print(f"\n--- {category} ---")
        assets = get_assets_for_category(category, ASSETS_PER_CATEGORY)
        if not assets:
            print(f"  No assets found for {category}, skipping.")
            all_failed += ASSETS_PER_CATEGORY
            continue

        for asset in assets:
            asset_id = asset.get("assetId", "unknown")
            display_name = asset.get("displayName", asset_id)
            
            download_url = find_download(asset, RESOLUTION)
            if not download_url:
                print(f"  No {RESOLUTION} download for {display_name}, trying lower res...")
                # Try 1K-JPG as fallback
                download_url = find_download(asset, "1K-JPG")
            
            if not download_url:
                print(f"  No suitable download for {display_name}, skipping.")
                all_failed += 1
                continue

            # Create subdirectory for this asset
            asset_dir = os.path.join(TEXTURES_DIR, asset_id)
            zip_filename = f"{asset_id}_{RESOLUTION}.zip"
            zip_path = os.path.join(TEXTURES_DIR, zip_filename)

            success = download_file(download_url, zip_path)
            if success:
                # Extract the zip into asset subdirectory
                extract_zip_in_place(zip_path, asset_dir)
                all_downloaded += 1
            else:
                print(f"  FAILED: {display_name}")
                all_failed += 1

            # Be nice to the API
            time.sleep(0.5)

    print("\n" + "=" * 60)
    print(f"Done! Downloaded: {all_downloaded}, Skipped: {all_skipped}, Failed: {all_failed}")
    print(f"Textures saved to: {TEXTURES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
