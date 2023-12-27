import time
import win32com.client
buffer_size=1024

def download_and_install_updates(updates_to_install,client_socket):
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
         # Create a Windows Update Downloader object
            update_downloader = update_session.CreateUpdateDownloader()
            update_downloader.Updates = updates_to_install

            client_socket.send(b'Downloading updates...')
            download_result = update_downloader.Download()

            if download_result.ResultCode == 2:
                client_socket.send(b'Downloaded updates successfully.')
            else:
                client_socket.send(b'Failed to download updates.')
                return

            # Create a Windows Update Installer object
            installer = update_session.CreateUpdateInstaller()
            installer.Updates = updates_to_install
            client_socket.send(b'Installing updates...')
            installation_result = installer.Install()

            for i, update in enumerate(updates_to_install):
                message=f"Installing update {i + 1}: {update.Title}"
                client_socket.send(message.encode())
            if installation_result.ResultCode == 2:
                client_socket.send(b'Installed updates successfully.')
            else:
                client_socket.send(b'Failed to install updates.')
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        client_socket.send(message.encode())
        client_socket.send(b'0')

def check_updates(client_socket):
    # Create a Windows Update Agent object
    update_session = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_session.CreateUpdateSearcher()
    try:
        client_socket.send(b'Searching for updates...')
        search_result = update_searcher.Search("IsInstalled=0 and Type='Software'")

        # Check if updates are available
        if search_result.Updates.Count > 0:
            message= f"Found {search_result.Updates.Count} updates."
            client_socket.send(message.encode())
            updates_to_install = search_result.Updates

            # Display the list of updates
            client_socket.send(b'List of updates:')
            for i, update in enumerate(updates_to_install):
                message=f"{i + 1}. {update.Title} "
                client_socket.send(message.encode())
        client_socket.send(b'Want to install updates?')
        time.sleep(0.2)
        client_socket.send(b'1.Yes')
        time.sleep(0.2)
        client_socket.send(b'2.No(return to meniu)')
        time.sleep(0.2)
        client_socket.send(b'rasp')
        rasp=client_socket.recv(buffer_size).decode()
        if rasp == '1':
            download_and_install_updates(updates_to_install)
        else:
            client_socket.send(b'0')
    except Exception as e:
        message = f"An error occurred: {str(e)}"
        client_socket.send(message.encode())
        client_socket.send(b'0')
        print(f"An error occurred: {str(e)}")