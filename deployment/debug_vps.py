import paramiko
import sys
import os

# Add current directory to path to import config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def run_command(ssh, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    if exit_status != 0:
        print(f"Error ({exit_status}): {err}")
    return out, err, exit_status

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {config.VPS_HOST}...")
    
    try:
        ssh.connect(config.VPS_HOST, username=config.VPS_USER, password=config.VPS_PASS)
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print("Checking Nginx config...")
    out, err, _ = run_command(ssh, "nginx -t")
    print(out)
    print(err)
    
    print("\nChecking sites-enabled/whatsapp.alkenacode.dev content:")
    out, _, _ = run_command(ssh, "cat /etc/nginx/sites-enabled/whatsapp.alkenacode.dev")
    print(out)
    
    ssh.close()

if __name__ == "__main__":
    main()
