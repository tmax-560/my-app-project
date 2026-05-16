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
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/commits/master"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers)
    data = res.json()
    if isinstance(data, list):
        return data[0]["sha"]
    return data["sha"]

def deploy():
    print("🔄 New commit detected! Deploying...")
    subprocess.run(["git", "pull"], check=True)
    subprocess.run(
        ["npm", "install", "--prefix", "app"],
        shell=True,
        check=True
    )
    subprocess.run(
        ["taskkill", "/f", "/im", "node.exe"],
        capture_output=True,
        shell=True
    )
    subprocess.Popen(
        r'"C:\Program Files\nodejs\node.exe" app\index.js',
        shell=True
    )
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



# Look for your loop and add these debug lines:
if latest_commit != current_commit:
    print(f"🚀 [DETECTED] New version found: {latest_commit}")
    
    # Check if the Git Pull actually works
    print("📥 Pulling new code...")
    os.system("git pull origin main")
    
    # Check if Docker is rebuilding
    print("🏗️ Rebuilding Docker image...")
    os.system("docker build -t my-app .")
    
    # Check if the container is restarting
    print("🔄 Restarting container...")
    os.system("docker stop my-app")
    os.system("docker rm my-app")
    os.system("docker run -d -p 3000:3000 --name my-app my-app")
    
    current_commit = latest_commit
else:
    print(f"😴 [IDLE] Still on version {current_commit}. No changes on GitHub.")