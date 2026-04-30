import subprocess
import time
import requests
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

GITHUB_USER = config["GITHUB_USER"]
GITHUB_REPO = config["GITHUB_REPO"]
GITHUB_TOKEN = config["GITHUB_TOKEN"]
CHECK_INTERVAL = 30  # seconds

last_sha = None

def get_latest_commit():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits/main"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers)
    return res.json()["sha"]

def deploy():
    print("🔄 New commit detected! Deploying...")
    subprocess.run(["git", "-C", "app", "pull"], check=True)
    subprocess.run(["npm", "install", "--prefix", "app"], check=True)
    # Restart app (kills old process, starts fresh)
    subprocess.run(["pkill", "-f", "node"], capture_output=True)
    subprocess.Popen(["node", "app/index.js"])
    print("✅ Deployment done!")

print("👀 Watching for new commits...")
while True:
    try:
        sha = get_latest_commit()
        if last_sha is None:
            last_sha = sha
            print(f"Tracking commit: {sha[:7]}")
        elif sha != last_sha:
            last_sha = sha
            deploy()
    except Exception as e:
        print(f"⚠️ Error: {e}")
    time.sleep(CHECK_INTERVAL)