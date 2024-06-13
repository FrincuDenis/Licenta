import psutil
import os


def find_process_by_name(name):
    """
    Return a list of processes matching 'name'.
    """
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            process_list.append(proc)
    return process_list


def kill_process_by_name(name):
    """
    Kill all processes matching 'name'.
    """
    process_list = find_process_by_name(name)
    if not process_list:
        print(f"No process with name '{name}' found.")
        return

    for proc in process_list:
        try:
            proc.kill()
            print(f"Process {proc.info['name']} with PID {proc.info['pid']} has been killed.")
        except psutil.NoSuchProcess:
            print(f"Process {proc.info['pid']} no longer exists.")
        except psutil.AccessDenied:
            print(f"Permission denied to kill process {proc.info['pid']}.")
        except Exception as e:
            print(f"An error occurred while killing process {proc.info['pid']}: {e}")


if __name__ == "__main__":
    process_name = input("Enter the process name to kill: ")
    kill_process_by_name(process_name)
