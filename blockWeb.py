
import os
import sys
import platform
import subprocess

def block_website(domain):
    """
    Blocks a website by adding an entry to the system's hosts file.
    """
    # Get the appropriate hosts file path based on the operating system
    if platform.system() == "Windows":
        hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
    elif platform.system() in ["Linux", "Darwin"]:
        hosts_file = "/etc/hosts"
    else:
        print(f"Unsupported operating system: {platform.system()}")
        return

    # Check if the domain is already blocked
    with open(hosts_file, "r") as file:
        if any(domain in line for line in file):
            print(f"{domain} is already blocked.")
            return

    # Add the domain to the hosts file
    with open(hosts_file, "a") as file:
        file.write(f"127.0.0.1 {domain}\n")
        print(f"{domain} has been blocked.")

def unblock_website(domain):
    """
    Unblocks a website by removing the entry from the system's hosts file.
    """
    # Get the appropriate hosts file path based on the operating system
    if platform.system() == "Windows":
        hosts_file = r"C:\Windows\System32\drivers\etc\hosts"
    elif platform.system() in ["Linux", "Darwin"]:
        hosts_file = "/etc/hosts"
    else:
        print(f"Unsupported operating system: {platform.system()}")
        return

    # Check if the domain is blocked
    with open(hosts_file, "r") as file:
        lines = file.readlines()

    # Remove the domain from the hosts file
    blocked = False
    with open(hosts_file, "w") as file:
        for line in lines:
            if domain not in line:
                file.write(line)
            else:
                blocked = True
    if blocked:
        print(f"{domain} has been unblocked.")
    else:
        print(f"{domain} was not blocked.")

if __name__ == "__main__":
    domain = input("Enter the domain to block: ").strip()
    block_website(domain)

    # If you want to unblock, you can use:
    # unblock_website(domain)
# Example usage:
#if __name__ == "__main__":
    #domain = input("Enter the domain to block: ").strip()
    #block_website_by_domain(domain)

    # If you want to unblock, you can use:
    # unblock_website_by_domain(domain)
