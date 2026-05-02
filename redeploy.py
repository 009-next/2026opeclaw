import paramiko
import sys
import io
import os
import zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SERVER = '47.74.33.22'
USER = 'root'
PASS = 'Inovatiebamabama0926gmail.com!'
LOCAL_DIR = r'c:\Users\ryoh0\AI\業務用\202604\202605\sitesim3d'
REMOTE_DIR = '/root/work/sitesim3d'
EXCLUDE_DIRS = {'node_modules', '.next', '.git'}
EXCLUDE_FILES = {'.env.local'}

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(LOCAL_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f in EXCLUDE_FILES:
                continue
            full = os.path.join(root, f)
            zf.write(full, os.path.relpath(full, LOCAL_DIR))
buf.seek(0)
print(f"Zip: {buf.getbuffer().nbytes // 1024} KB")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER, username=USER, password=PASS, timeout=15)
sftp = ssh.open_sftp()

def run(cmd, timeout=300):
    print(f"$ {cmd[:100]}")
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    if out:
        for line in out.strip().split('\n')[-10:]:
            print(f"  {line}")
    if err:
        for line in err.strip().split('\n')[-5:]:
            print(f"  [err] {line}")
    return out

print("Uploading...")
with sftp.file('/root/work/sitesim3d.zip', 'wb') as f:
    f.write(buf.read())

run(f'cd {REMOTE_DIR} && unzip -o /root/work/sitesim3d.zip && rm /root/work/sitesim3d.zip')
run(f'cd {REMOTE_DIR} && npm run build')
run('systemctl restart sitesim3d')

import time
time.sleep(3)
run('curl -s http://localhost:3100/ -o /dev/null -w "HTTP %{http_code}"')

sftp.close()
ssh.close()
print("\nDone! https://47.74.33.22/sim/")
