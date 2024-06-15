import json
import subprocess

class UserManager:
    def __init__(self):
        self.users = []
        self.all_users_info = {}

    def get_all_users(self):
        try:
            # Run 'net user' command to get all users
            result = subprocess.run(['net', 'user'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                    shell=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return []

            # Parse the result to get the list of users
            output = result.stdout.splitlines()
            capture = False

            for line in output:
                line = line.strip()
                if line.startswith('---'):
                    capture = True
                    continue
                if capture:
                    if line == '' or line == 'The command completed successfully.':
                        break
                    self.users.extend(line.split())

            return self.users
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_user_info(self, username):
        try:
            # Run 'net user <username>' command to get user info
            result = subprocess.run(['net', 'user', username], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, shell=True)
            if result.returncode != 0:
                print(f"Error fetching info for user {username}: {result.stderr}")
                return None

            # Parse the result to get the user info
            output = result.stdout.splitlines()
            user_info = {}

            # List of fields to extract
            fields_of_interest = {
                'User name': 'Name',
                'Full Name': 'Full Name',
                'Comment': 'Comment',
                "User's comment": "User's comment",
                'Account active': 'Account active',
                'Account expires': 'Account expires',
                'Password last set': 'Password last set',
                'Password expires': 'Password expires',
                'Password changeable': 'Password changeable',
                'Password required': 'Password required',
                'Last logon': 'Last logon',
                'Local Group Memberships': 'Local Group Memberships'
            }

            # Skip the first two lines and the last line which is the confirmation message
            for line in output:
                if line.strip() and line.strip() != 'The command completed successfully.':
                    parts = line.split('  ', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        if key in fields_of_interest:
                            user_info[fields_of_interest[key]] = value

            return user_info
        except Exception as e:
            print(f"An error occurred while fetching info for user {username}: {e}")
            return None

    def fetch_all_user_info(self):
        # print("Fetching all users...")
        self.get_all_users()

        if self.users:
            # print("Users found:")
            # Get info for each user
            for specific_user in self.users:
                # print(f"\nFetching info for user: {specific_user}")
                user_info = self.get_user_info(specific_user)
                if user_info:
                    self.all_users_info[specific_user] = user_info
                    # print(f"Info for user {specific_user}:")
                    fields_to_print = [
                        'Name', 'Full Name', 'Comment', "User's comment", 'Account active', 'Account expires',
                        'Password last set',
                        'Password expires', 'Password changeable', 'Password required',
                        'Last logon', 'Local Group Memberships'
                    ]
                    #for field in fields_to_print:
                        #if field in user_info:
                            #print(f"{field}: {user_info[field]}")
                else:
                    print(f"Could not retrieve info for user: {specific_user}")
        else:
            print("No users found or an error occurred.")

    def add_user(self, username, password, full_name=None, description=None, set_active=True, group=None):
        try:
            # Construct the base command as a string
            command = f'net user {username} {password} /ADD'

            # Append the full name option if provided
            if full_name:
                command += f' /FULLNAME:"{full_name}"'

            # Append the comment/description option if provided
            if description:
                command += f' /COMMENT:"{description}"'

            # Append the active/inactive option
            if not set_active:
                command += ' /ACTIVE:NO'
            else:
                command += ' /ACTIVE:YES'

            # Run the command to add the user
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

            # Check the result of the user creation command
            if result.returncode == 0:
                print(f"User {username} added successfully.")
                # If the user was added successfully, add the user to the specified group if provided
                if group:
                    group_command = f'net localgroup {group} {username} /ADD'
                    group_result = subprocess.run(group_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                  text=True, shell=True)
                    if group_result.returncode == 0:
                        print(f"User {username} added to group {group} successfully.")
                    else:
                        print(f"Error adding user {username} to group {group}: {group_result.stderr}")
            else:
                print(f"Error adding user {username}: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while adding user {username}: {e}")

    def remove_user(self, username):
        try:
            # Run 'net user <username> /DELETE' command to remove user
            result = subprocess.run(['net', 'user', username, '/DELETE'], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, shell=True)
            if result.returncode == 0:
                print(f"User {username} removed successfully.")
            else:
                print(f"Error removing user {username}: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while removing user {username}: {e}")

    def is_in_domain(self):
        try:
            # Run PowerShell command to check if the computer is in a domain and get the domain name and PartOfDomain status
            result = subprocess.run(
                ['powershell', '-Command',
                 '(Get-WmiObject Win32_ComputerSystem | Select-Object -Property Domain, PartOfDomain | ConvertTo-Json)'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

            if result.returncode != 0:
                print(f"Error checking domain status: {result.stderr}")
                return {"PartOfDomain": False, "DomainName": None}

            # Parse the JSON output
            output = json.loads(result.stdout.strip())

            domain_name = output.get('Domain', '')
            part_of_domain = output.get('PartOfDomain', False)

            if part_of_domain:
               # print(f"Computer is in domain: {domain_name}")
                return {"PartOfDomain": part_of_domain, "DomainName": domain_name}
            else:
                #print("Computer is not in a domain")
                return {"PartOfDomain": part_of_domain, "DomainName": None}
        except Exception as e:
            print(f"An error occurred while checking domain status: {e}")
            return {"PartOfDomain": False, "DomainName": None}

    def add_to_domain(self, domain, username, password):
        try:
            # Run PowerShell command to add the computer to a domain
            command = f"Add-Computer -DomainName {domain} -Credential (New-Object System.Management.Automation.PSCredential('{username}', (ConvertTo-SecureString '{password}' -AsPlainText -Force))) -Force -Restart"
            result = subprocess.run(['powershell', '-Command', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, shell=True)
            if result.returncode == 0:
               print(f"Computer successfully added to domain {domain}.")
            else:
                print(f"Error adding computer to domain {domain}: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while adding computer to domain {domain}: {e}")

    def remove_from_domain(self, local_admin, local_password):
        try:
            # Run PowerShell command to remove the computer from a domain
            command = f"Remove-Computer -UnjoinDomaincredential (New-Object System.Management.Automation.PSCredential('{local_admin}', (ConvertTo-SecureString '{local_password}' -AsPlainText -Force))) -Force -Restart"
            result = subprocess.run(['powershell', '-Command', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, shell=True)
            if result.returncode == 0:
                print("Computer successfully removed from domain.")
            else:
                print(f"Error removing computer from domain: {result.stderr}")
        except Exception as e:
            print(f"An error occurred while removing computer from domain: {e}")

    def get_local_groups(self):
        try:
            # Execute the command to get local groups
            result = subprocess.run(['net', 'localgroup'], capture_output=True, text=True, check=True)

            # Split the output by lines
            output_lines = result.stdout.splitlines()

            # The groups are listed after a specific header line and before a specific footer line
            header = "Aliases for"
            footer = "The command completed successfully."

            # Find the start and end indices
            start_index = next(i for i, line in enumerate(output_lines) if line.startswith(header)) + 2
            end_index = next(i for i, line in enumerate(output_lines) if line.startswith(footer))

            # Extract the group names, excluding the separator line and removing the '*'
            groups = [line.replace('*', '').strip() for line in output_lines[start_index:end_index] if
                      line.strip() and line != "-------------------------------------------------------------------------------"]

            return {"Name of the group": groups}
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while fetching local groups: {e}")
            return {}
        except StopIteration:
            print("Unexpected output format. Failed to parse local groups.")
            return {}
