import paramiko
import time

# Informasi instance
public_ip = 'your_instance_public_ip'  # Ganti dengan Public IP instance yang baru dibuat
key_path = '/path/to/your-key-pair.pem'  # Ganti dengan path ke private key Anda
username = 'ubuntu'  # Ganti dengan username yang sesuai (Ubuntu pada EC2 biasanya 'ubuntu')

# Fungsi untuk SSH ke instance dan mengonfigurasi proxy
def setup_proxy(public_ip):
    print(f"Terhubung ke instance dengan IP: {public_ip}")
    
    # Gunakan Paramiko untuk mengakses instance via SSH
    key = paramiko.RSAKey.from_private_key_file(key_path)  # Path ke private key file
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(public_ip, username=username, pkey=key)

    # Install Squid Proxy di VPS
    commands = [
        "sudo apt-get update -y",
        "sudo apt-get install squid -y",
        "sudo service squid start",
        "sudo ufw allow 3128/tcp"  # Port default untuk Squid
    ]
    
    for command in commands:
        print(f"Menjalankan command: {command}")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

    print("Proxy server Squid telah terinstal dan dijalankan.")
    ssh_client.close()

# Main function untuk setup proxy
def main():
    setup_proxy(public_ip)

if __name__ == '__main__':
    main()
