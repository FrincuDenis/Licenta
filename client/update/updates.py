import time
import win32com.client
from client import rcv
buffer_size=1024

def download_and_install_updates(updates_to_install,client_socket,public_key):
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
         # Create a Windows Update Downloader object
            update_downloader = update_session.CreateUpdateDownloader()
            update_downloader.Updates = updates_to_install

            rcv.send_msg('Downloading updates...', client_socket, public_key)
            download_result = update_downloader.Download()

            if download_result.ResultCode == 2:
                rcv.send_msg('Downloaded updates successfully.', client_socket, public_key)
            else:
                rcv.send_msg('Failed to download updates.', client_socket, public_key)
                return

            # Create a Windows Update Installer object
            installer = update_session.CreateUpdateInstaller()
            installer.Updates = updates_to_install
            rcv.send_msg('Installing updates...', client_socket, public_key)
            installation_result = installer.Install()

            for i, update in enumerate(updates_to_install):
                message=f"Installing update {i + 1}: {update.Title}"
                rcv.send_msg(message, client_socket, public_key)
            if installation_result.ResultCode == 2:
                rcv.send_msg('Installed updates successfully.', client_socket, public_key)
            else:
                rcv.send_msg('Failed to install updates.', client_socket, public_key)
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        rcv.send_msg(message, client_socket, public_key)
        client_socket.send('0')

def check_updates(client_socket,public_key):
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
        rcv.send_msg('Searching for updates...', client_socket, public_key)
        search_result = update_searcher.Search("IsInstalled=0 and Type='Software'")

        # Check if updates are available
        if search_result.Updates.Count > 0:
            message= f"Found {search_result.Updates.Count} updates."
            client_socket.send(message.encode())
            updates_to_install = search_result.Updates

            # Display the list of updates
            rcv.send_msg('List of updates:', client_socket, public_key)
            for i, update in enumerate(updates_to_install):
                message=f"{i + 1}. {update.Title} "
                rcv.send_msg(message, client_socket, public_key)
        rcv.send_msg('Want to install updates?', client_socket, public_key)
        time.sleep(0.2)
        rcv.send_msg('1.Yes', client_socket, public_key)
        time.sleep(0.2)
        rcv.send_msg('2.No(return to meniu)', client_socket, public_key)
        time.sleep(0.2)
        rcv.send_msg('rasp', client_socket, public_key)
        rasp=client_socket.recv(buffer_size).decode()
        if rasp == '1':
            download_and_install_updates(updates_to_install,client_socket,public_key)
        else:
            client_socket.send('0')
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        client_socket.send(message.encode())
        client_socket.send('0')
        print(f"An error occurred: {str(e)}")