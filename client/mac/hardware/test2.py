import subprocess

def get_disk_names():
    disk_names = []
    try:
        diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
        lines = diskutil_output.split("\n")
        for line in lines:
            if "disk" in line:
                disk_name = line.split()[0]
                disk_names.append(disk_name)
    except subprocess.CalledProcessError:
        print("Error: Failed to execute diskutil command.")
    return disk_names

if __name__ == "__main__":
    disk_names = get_disk_names()
    print("Disk names:", disk_names)
