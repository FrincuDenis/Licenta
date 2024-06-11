import subprocess

def add_user(username, password, full_name=None, description=None):
    try:
        # Construct the base command as a string
        command = f'net user {username} {password} /ADD'

        # Append the full name option if provided
        if full_name:
            command += f' /FULLNAME:"{full_name}"'

        # Append the comment/description option if provided
        if description:
            command += f' /COMMENT:"{description}"'

        # Run the command in the shell
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # Check the result
        if result.returncode == 0:
            print(f"User {username} added successfully.")
        else:
            print(f"Error adding user {username}: {result.stderr}")
    except Exception as e:
        print(f"An error occurred while adding user {username}: {e}")

# Example usage
add_user('testuser', 'testpassword', 'John Doe', 'Test user account')
