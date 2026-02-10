import paramiko
import sys
import os
import re

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

    # Check port 4577
    print("Checking port 4577...")
    # Using netstat -tuln to see listening ports. 
    # Docker might not be running yet, so port might be free. 
    # User said "check if port 4577 ... are in use... I've updated docker mapping...".
    # If docker is running, it should be in use. If not, it's free.
    # The instruction implies verification. I'll just report it.
    out, _, _ = run_command(ssh, "netstat -tuln | grep :4577")
    if out:
        print(f"Port 4577 is currently in use:\n{out}")
    else:
        print("Port 4577 is NOT currently in use.")

    # Read wandola config
    template_site = "wandolaenergysystems.co.ke"
    target_site = "whatsapp.alkenacode.dev"
    
    print(f"Reading {template_site} config...")
    cmd = f"cat /etc/nginx/sites-available/{template_site}"
    wandola_conf, err, status = run_command(ssh, cmd)
    if status != 0:
        print("Failed to read config. Exiting.")
        return

    # Modify config
    print("Modifying configuration...")
    new_conf_lines = []
    lines = wandola_conf.split('\n')
    
    # We want to keep the file structure but remove SSL and update port
    # Remove SSL blocks usually at the end managed by Certbot
    # And remove simple 'listen 443 ssl' directives if we are starting fresh
    
    for line in lines:
        # Skip lines related to SSL certificates
        if "ssl_certificate" in line or "ssl_certificate_key" in line or "managed by Certbot" in line:
            continue
        
        # If the line is 'listen 443 ssl;', skip it as we want Certbot to add it fresh
        if "listen 443 ssl" in line:
            continue
            
        # Update server_name
        if "server_name" in line:
            # Replace the server name with ours
            # It might have multiple names, but we'll specific set ours
            line = re.sub(r"server_name\s+.*;", f"server_name {target_site};", line)

        # Update root / location proxy_pass
        if "proxy_pass" in line:
            # Look for http://...:PORT...
            # We want to replace the PORT with 4577
            # Capture the structure to preserve trailing slash if present
            # Pattern: http://(ip|localhost):(\d+)(/?.*)
            match = re.search(r"(http://[^:]+):(\d+)(.*);", line)
            if match:
                base = match.group(1) # http://localhost
                old_port = match.group(2)
                rest = match.group(3) # / or empty
                
                # Check if we are in 'location /' block?
                # The prompt says "update the ports for / it be 4577".
                # Simple replacement for all proxy_pass might be safer if there is only one app.
                # Assuming standard config.
                
                new_line = line.replace(f":{old_port}", ":4577")
                line = new_line

        new_conf_lines.append(line)
        
    new_conf_content = "\n".join(new_conf_lines)
    
    # Write to file
    print(f"Writing new config to /etc/nginx/sites-available/{target_site}...")
    # Construct a safe echo command.
    # We can write to a temp file using sftp to avoid escaping hell
    sftp = ssh.open_sftp()
    with sftp.file(f"/tmp/{target_site}", 'w') as f:
        f.write(new_conf_content)
    
    # Move it to sites-available
    run_command(ssh, f"mv /tmp/{target_site} /etc/nginx/sites-available/{target_site}")
    
    # Link it
    print("Linking site...")
    run_command(ssh, f"ln -sf /etc/nginx/sites-available/{target_site} /etc/nginx/sites-enabled/")
    
    # Reload nginx
    print("Reloading Nginx...")
    run_command(ssh, "nginx -t && systemctl reload nginx")
    
    # Certbot
    print("Running Certbot...")
    # Use config email or a default
    email = "info@alkenacodecreations.co.ke"
    certbot_cmd = f"certbot --nginx -d {target_site} --non-interactive --agree-tos -m {email}"
    out, err, status = run_command(ssh, certbot_cmd)
    print(out)
    if status != 0:
        print(f"Certbot failed: {err}")

    ssh.close()
    print("Done.")

if __name__ == "__main__":
    main()
