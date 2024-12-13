import boto3
import time

# Setup AWS Boto3 client
ec2 = boto3.client('ec2', region_name='us-west-1')  # Ganti dengan region AWS Anda
key_name = 'ORA.pem'  # Ganti dengan nama key pair AWS Anda
ami_id = 'ami-0e2c8caa4b6378d8c'  # Ganti dengan ID AMI yang sesuai (misalnya, Ubuntu 20.04)
instance_type = 't2.micro'  # Ganti dengan instance type yang sesuai (t2.micro untuk Free Tier)
security_group_id = 'sg-0df852efd3ff18104'  # Ganti dengan ID security group yang sesuai

# 1. Membuat EC2 instance
def create_ec2_instance():
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        KeyName=key_name,
        SecurityGroupIds=[security_group_id],
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'MyProxyVPS'}
            ]
        }]
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 Instance {instance_id} telah dibuat.")
    return instance_id

# 2. Menunggu hingga instance siap
def wait_for_instance(instance_id):
    waiter = ec2.get_waiter('instance_running')
    print("Menunggu instance siap...")
    waiter.wait(InstanceIds=[instance_id])
    print("Instance siap.")
    
    # Mendapatkan Public IP instance
    instance_info = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = instance_info['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return public_ip

# Main function untuk membuat VPS
def main():
    # Langkah 1: Membuat EC2 instance
    instance_id = create_ec2_instance()
    
    # Langkah 2: Tunggu hingga instance siap
    public_ip = wait_for_instance(instance_id)
    print(f"Public IP dari instance EC2: {public_ip}")

if __name__ == '__main__':
    main()
