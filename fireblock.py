

import subprocess



def resolve_ip(domain):
    command = 'nslookup'
    args = [domain]

    full_command = [command] + args

    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    output = result.stdout


    lines = output.strip().split("\n")
    print (lines)

    server = lines[0].split(": ")[1].strip()
    address = lines[1].split(": ")[1].strip()

    addresses = []
    addresses.append(lines[4].split(':  ')[1])
    for line in lines[4:]:
        if line.startswith("Addresses:"):
            continue
        if line.startswith('Aliases:'):
            continue
        if line.startswith("\t"):
            addresses.append(line.strip())

        else:
            for addr in line.split(":")[1].strip().split(","):
                addresses.append(addr.strip())

    print("Addresses:")
    for addr in addresses:
        print(f"- {addr}")
    return addresses

def add_firewall_rule(domain, ips):
    ips_str = ",".join(ips)
    try:
        command = f'netsh advfirewall firewall add rule name="Block {domain}" dir=out action=block remoteip={ips_str} protocol=ANY profile=any'
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully blocked {domain}with IP {ips_str}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block {domain}with IP {ips_str}")
        print(f"Error: {e}")


def block_website_by_domain(domain):
    addresses = resolve_ip(domain)
    ipv_addresses = addresses

    if not addresses:
        print(f"Unable to resolve the domain {domain}. Aborting...")
        return


    add_firewall_rule(domain, addresses)

if __name__ == "__main__":
    domain = input("Enter the domain to block: ").strip()
    block_website_by_domain(domain)
