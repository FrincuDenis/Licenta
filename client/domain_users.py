
import win32net
import win32netcon
import win32security
import subprocess
def add_local_user(username, password):
    user_info = {
        'name': username,
        'password': password,
        'priv': win32netcon.USER_PRIV_USER,
        'flags': win32netcon.UF_NORMAL_ACCOUNT
    }
    win32net.NetUserAdd(None, 1, user_info)

def modify_local_user(username, password):
    user_info = {
        'password': password
    }
    win32net.NetUserSetInfo(None, username, 2, user_info)

def remove_local_user(username):
    win32net.NetUserDel(None, username)

def add_to_group(username, group_name):
     command = f"net localgroup {group_name} {username} /add"
     try:
        result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        print("User added successfully.")
     except subprocess.CalledProcessError as e:
        print(f"Failed to add user: {e.stderr}")

def join_domain(domain, username, password):
    command = f"Add-Computer -DomainName {domain} -Credential (New-Object System.Management.Automation.PSCredential('{username}', (ConvertTo-SecureString '{password}' -AsPlainText -Force)))"
    subprocess.run(["powershell", "-Command", command])

def remove_from_domain(username, password):
    command = f"Remove-Computer -UnjoinDomainCredential (Get-Credential) -WorkgroupName WORKGROUP -Credential (New-Object System.Management.Automation.PSCredential('{username}', (ConvertTo-SecureString '{password}' -AsPlainText -Force))) -Force -Restart"
    subprocess.run(["powershell", "-Command", command])

while True:
    stelar=input()
    if stelar == '1':
        add_local_user("testuser", "password123")
    elif stelar == '2':
        modify_local_user("testuser", "newpassword456")
    elif stelar == '3':
        remove_local_user("testuser")
    elif stelar == '4':
        add_to_group("testuser", "Administrators")
    elif stelar == '5':
        join_domain("e-uvt.ro", "admin", "adminpassword")
    elif stelar == '6':
        remove_from_domain("admin", "adminpassword")




