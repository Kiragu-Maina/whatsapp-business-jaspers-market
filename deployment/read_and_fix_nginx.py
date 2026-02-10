import paramiko
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def run_command(ssh, command):
    print(f"Running: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    out = stdout.read().decode().strip()
    return out

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(config.VPS_HOST, username=config.VPS_USER, password=config.VPS_PASS)

    print("Reading current config...")
    # Read the file we created
    content = run_command(ssh, "cat /etc/nginx/sites-available/whatsapp.alkenacode.dev")
    print("Current Content:\n" + content)
    
    # Fix the proxy_pass line
    new_lines = []
    for line in content.split('\n'):
        if "proxy_pass" in line:
            # Replace whatever url with http://localhost:4577
            # Preserve indentation
            indent = line[:line.find("proxy_pass")]
            # Check for trailing slash
            if line.strip().endswith("/;"): 
                 new_lines.append(f"{indent}proxy_pass http://localhost:4577/;")
            else:
                 new_lines.append(f"{indent}proxy_pass http://localhost:4577;")
        else:
            new_lines.append(line)
            
    new_content = "\n".join(new_lines)
    print("\nNew Content:\n" + new_content)
    
    # Write back
    sftp = ssh.open_sftp()
    with sftp.file("/tmp/whatsapp_fix", 'w') as f:
        f.write(new_content)
        
    run_command(ssh, "mv /tmp/whatsapp_fix /etc/nginx/sites-available/whatsapp.alkenacode.dev")
    run_command(ssh, "nginx -t && systemctl reload nginx")
    
    # Run Certbot again
    print("Running Certbot...")
    out = run_command(ssh, "certbot --nginx -d whatsapp.alkenacode.dev --non-interactive --agree-tos -m info@alkenacodecreations.co.ke")
    print(out)
    
    ssh.close()

if __name__ == "__main__":
    main()
