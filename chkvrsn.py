import os
import subprocess

def check_sysmon_installation():
    sysmon_path = r'C:\Windows\sysmon64.exe'

    # Check if sysmon64.exe exists in the specified path
    if os.path.exists(sysmon_path):
        try:
            # Get the version of sysmon64.exe using PowerShell
            command = f'powershell.exe (Get-Command "{sysmon_path}").FileVersionInfo.ProductVersion'
            result = subprocess.run(command, capture_output=True, text=True)
            version = result.stdout.strip()

            return True, version

        except Exception as e:
            return False, str(e)

    else:
        return False, "Sysmon64 is not installed."

# Check if Sysmon64 is installed and get the version
is_installed, version = check_sysmon_installation()

# Print the result
if is_installed:
    print(f"Sysmon is installed (Version: {version})")
else:
    print(f"Sysmon is not installed")

