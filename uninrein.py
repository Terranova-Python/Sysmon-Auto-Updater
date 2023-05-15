''' Script Created by Anthony Terrano (TerranovaTech) 5/15/2023'''
import os, subprocess, ctypes, sys

# Checks to see if the user running this script can run an elevated CMD
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except Exception as e:
        print(f"An error occurred while checking admin privileges: {e}")
        return False


# Stops the service before trying to uninstall - Otherwise it wont
def stop_sysmon_service():
    try:
        # Stop the Sysmon service using PowerShell
        command = 'powershell.exe Stop-Service -Name Sysmon'
        subprocess.run(command, capture_output=True, text=True)

        return True

    except Exception as e:
        print(f"An error occurred while stopping the Sysmon service: {e}")
        return False


# Uninstalls Sysmon by running an elevated command in the same Directory as it was installed (C:\Windows\)
def uninstall_sysmon():
    try:
        # Stop the Sysmon service
        if stop_sysmon_service():
            # Check if script is running as administrator
            if not is_admin():
                print("Script is not running with administrator privileges. Restarting as administrator...")
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()

            # Change directory to C:\Windows\
            os.chdir('C:\\Windows\\')

            # Run sysmon64.exe uninstall command
            command = 'sysmon64.exe -u force'
            subprocess.run(command, capture_output=True, text=True)

            return True

    except Exception as e:
        print(f"An error occurred during uninstallation: {e}")
        return False


# Once uninstalled, it tries to install from a new location (C:\SysmonUpdate\sysmon64)
def install_sysmon():
    try:
        # Change directory to the location of sysmon64.exe
        os.chdir('C:\\SysmonUpdate')

        # Install sysmon64.exe
        command = 'sysmon64.exe -accepteula -i'
        subprocess.run(command, capture_output=True, text=True)

        return True

    except Exception as e:
        print(f"An error occurred during installation: {e}")
        return False

# Uninstall Sysmon64
if uninstall_sysmon():
    print("Sysmon64 has been uninstalled.")

# Install new version of Sysmon64
if install_sysmon():
    print("Sysmon64 has been installed.")
