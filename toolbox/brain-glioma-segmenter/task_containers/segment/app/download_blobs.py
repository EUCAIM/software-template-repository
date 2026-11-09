import os
import urllib.request
import sys
import subprocess
import hashlib
import zipfile
import json
import shutil
import time

# Configuration file path
CONFIG_FILE = "blobs_config.json"

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config file {CONFIG_FILE}: {e}")
        sys.exit(1)

def check_md5(file_path, expected_md5):
    if not expected_md5:
        return True
    print(f"Verifying MD5 for {file_path}...")
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest() == expected_md5

def download_file(url, dest_path, expected_md5=None):
    print(f"Downloading {url} to {dest_path}...")
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        # Create request with optional authorization header
        req = urllib.request.Request(url)
        token = os.environ.get("WEIGHTS_TOKEN")
        if token:
            print("Using authorization token from environment variable.")
            # Check if it's a Hugging Face token (starts with hf_) or generic
            if token.startswith("hf_"):
                req.add_header("Authorization", f"Bearer {token}")
            else:
                # Generic Basic Auth or other schemes could be added here
                req.add_header("Authorization", f"Bearer {token}")

        with urllib.request.urlopen(req) as response:
            total_size = int(response.info().get('Content-Length', 0))
            block_size = 8192 * 4  # 32KB blocks
            downloaded = 0
            start_time = time.time()
            last_print_time = start_time

            with open(dest_path, 'wb') as out_file:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    downloaded += len(buffer)
                    out_file.write(buffer)
                    
                    # Print progress every 5 seconds
                    current_time = time.time()
                    if current_time - last_print_time > 5:
                        if total_size > 0:
                            percent = downloaded * 100 / total_size
                            mb_downloaded = downloaded / (1024 * 1024)
                            mb_total = total_size / (1024 * 1024)
                            print(f"Progress: {percent:.1f}% ({mb_downloaded:.1f}MB / {mb_total:.1f}MB)")
                        else:
                            mb_downloaded = downloaded / (1024 * 1024)
                            print(f"Downloaded: {mb_downloaded:.1f}MB")
                        last_print_time = current_time
            
        print(f"Successfully downloaded {dest_path}")
        
        if expected_md5:
            if check_md5(dest_path, expected_md5):
                print(f"MD5 verified for {dest_path}")
            else:
                print(f"MD5 mismatch for {dest_path}!")
                sys.exit(1)
                
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        sys.exit(1)

def unzip_file(zip_path, extract_to):
    print(f"Unzipping {zip_path} to {extract_to}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Successfully extracted {zip_path}")
        # Remove zip file to save space
        print(f"Removing {zip_path} to save space...")
        os.remove(zip_path)
    except Exception as e:
        print(f"Failed to unzip {zip_path}: {e}")
        sys.exit(1)

def main():
    print("Starting weight download...")
    
    config = load_config()
    weights_urls = config.get("weights_urls", {})
    weights_md5 = config.get("weights_md5", {})
    dest_dir = config.get("dest_dir", "/mlcube_inferer/checkpoints")
    check_extracted = config.get("check_extracted", None)
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Check if weights are already extracted
    if check_extracted:
        check_path = os.path.join(dest_dir, check_extracted)
        if os.path.exists(check_path):
            print(f"Found existing weights at {check_path}. Skipping download.")
            # Skip the download loop entirely
            weights_urls = {} 

    for filename, url in weights_urls.items():
        dest_path = os.path.join(dest_dir, filename)
        
        if os.path.exists(dest_path):
            print(f"File {filename} already exists. Skipping download.")
        else:
            download_file(url, dest_path, weights_md5.get(filename))
        
        unzip_file(dest_path, dest_dir)

    print("All weights ready.")

    # Pass arguments to the actual runner
    # The Dockerfile CMD passes arguments to this script, which we forward to runner.py
    cmd = ["python", "runner.py"] + sys.argv[1:]
    print(f"Executing: {' '.join(cmd)}")
    
    # Replace the current process with runner.py
    # This ensures runner.py becomes PID 1 (or the main process)
    try:
        # We need to be in the correct directory for runner.py
        os.chdir("/mlcube_project")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
