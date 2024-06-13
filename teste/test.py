import json
import subprocess

def is_in_domain():
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
            #print(f"Computer is in domain: {domain_name}")
            return {"PartOfDomain": part_of_domain, "DomainName": domain_name}
        else:
            #print("Computer is not in a domain")
            return {"PartOfDomain": part_of_domain, "DomainName": None}
    except Exception as e:
        print(f"An error occurred while checking domain status: {e}")
        return {"PartOfDomain": False, "DomainName": None}

is_in_domain()