import ipaddress
import kemp_agent
import cf_agent

if __name__ == "__main__":
    name = input("Enter a name for the App (alpha-numeric): ")
    name = "".join(e for e in name.strip() if e.isalnum())
    if not name:
        raise ValueError("Invalid name. Please enter a valid alpha-numeric name.")

    domain = input("Enter the full domain for the App (ex: app_name.example.com): ")
    domain = domain.strip()
    if not domain:
        raise ValueError("Invalid domain. Please enter a valid domain.")

    real_server = input(
        "Enter the IP address where the app is hosted (ex: 192.168.1.100): "
    )
    real_server = real_server.strip()

    try:
        ipaddress.ip_address(real_server)
    except ValueError:
        raise ValueError(
            f"Invalid IP address format: {real_server}. Please enter a valid IP address."
        )

    real_port = input("Enter the port number (ex: 443 or 8443): ")
    real_port = real_port.strip()
    if not real_port.isdigit() or not (1 <= int(real_port) <= 65535):
        raise ValueError(
            "Invalid port number. Please enter a valid port between 1 and 65535."
        )
    
    dns_entry = input("Create DNS entry for this app? (y/n): ").strip().lower()

    # Confirmation
    print("=========================================")
    print(f"Creating App with the following details:")
    print(f"Name: {name}")
    print(f"Domain: {domain}")
    print(f"Real Server: {real_server}")
    print(f"Real Port: {real_port}")
    print(f"Create DNS Entry: {dns_entry}")
    print("=========================================")

    confirmation = input("Proceed? (y/n): ").strip().lower()
    if confirmation != "y":
        print("Operation cancelled.")
        exit(0)

    # Create the app in Kemp Virtual LoadMaster
    kemp_agent.add_rule(domain, name)
    vs_index = kemp_agent.add_subvs()
    kemp_agent.mod_subvs(vs_index, name)
    kemp_agent.add_real_server(vs_index, real_server, real_port)

    if dns_entry == "y":
        cf_agent.create_dns_record(domain)

    print(
        "\n App created successfully.\nRemember to link the rule to the new SubVS manually in the WebUI!"
    )
    input("Press Enter to exit...")
