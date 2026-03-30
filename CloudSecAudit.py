import boto3
import json  
from datetime import datetime
import sys

iam = boto3.client('iam')
s3 = boto3.client('s3')

BUCKET_NAME = 'chris-cloud-information'

def audit_to_files():
    print("\n---STEP 1: SCANNING AWS USERS ---")
    
    try:
        users = iam.list_users()['Users']
    except Exception as e:
        print(f"CRITICAL ERROR: Could not connect to AWS. {e}")
        return

    all_results = [] 
    for user in users:
        username = user['UserName']
        
        user_data = {
            "user": username,
            "status": "Safe", 
            "risks": []
        }

        
        policies = iam.list_attached_user_policies(UserName=username)['AttachedPolicies']
        for p in policies:
            if p['PolicyName'] == 'AdministratorAccess':
                user_data["status"] = "CRITICAL"
                user_data["risks"].append("User has AdministratorAccess policy")

        groups = iam.list_groups_for_user(UserName=username)['Groups']
        for group in groups:
            g_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']
            for gp in g_policies:
                if gp['PolicyName'] == 'AdministratorAccess':
                    user_data["status"] = "CRITICAL"
                    user_data["risks"].append(f"Admin power via Group: {group['GroupName']}")

        all_results.append(user_data)
        
    json_file = f"audit_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w") as f:
        json.dump(all_results, f, indent=4)
    print(f"STEP 2: Local file '{json_file}' created.")

    print(f"---STEP 3: UPLOADING TO BUCKET [{BUCKET_NAME}] ---")
    try:
        s3.upload_file(json_file, BUCKET_NAME, json_file)
        print("STEP 3: File is officially in the cloud.")
    except Exception as e:
        print(f"UPLOAD FAILED: {e}")
        print("Wrong Bucket Name, No S3 Permissions, or No Internet.")

if __name__ == "__main__":
    audit_to_files()

    