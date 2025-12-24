# Kemp-SubVS-Launch

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![uv](https://img.shields.io/badge/uv-purple?style=for-the-badge&logo=uv&logoColor=%23DE5FE9)

Kemp-SubVS-Launch is an automated deployment tool for Kemp Virtual LoadMaster that streamlines the process of adding new applications to your load balancer. With a simple command-line interface, it creates the domain rule, sets up a Sub-Virtual Service (SubVS), configures the real server, and optionally creates a DNS A record in Cloudflare.

Perfect for quickly deploying new services behind your Kemp LoadMaster without manual configuration through the WebUI.

## Features

- **Automated SubVS Creation** - Creates and configures a new Sub-Virtual Service with a single command
- **Domain Rule Setup** - Automatically creates content rules for domain-based routing
- **Real Server Configuration** - Adds and configures backend servers with specified ports
- **Optional DNS Management** - Creates Cloudflare DNS A records for your new application
- **Interactive CLI** - Simple prompts guide you through the setup process
- **Input Validation** - Validates IP addresses, port numbers, and domain names

### Prerequisites
- Kemp Virtual LoadMaster with API access enabled
- Cloudflare account (optional, for DNS management)

## How It Works

When you run the application, it will:

1. **Prompt for Application Details**
   - Application name (alphanumeric only)
   - Full domain name (e.g., app.example.com)
   - Backend server IP address
   - Backend server port
   - Whether to create a DNS record

2. **Create Domain Rule**
   - Adds a content rule in Kemp for host-based routing
   - Uses regex pattern matching for the specified domain

3. **Create Sub-Virtual Service**
   - Generates a new SubVS under your main Virtual Service
   - Configures with a friendly nickname
   - Sets HTTP health check method to GET

4. **Add Real Server**
   - Adds your backend server to the SubVS
   - Configures the specified port
   - Sets TCP protocol

5. **Create DNS Record (Optional)**
   - Creates an A record in Cloudflare
   - Points to your public IP address
   - Enables Cloudflare proxy

## Important Note

After running the tool successfully, you must manually link the content rule to the new SubVS in the Kemp WebUI:

1. Navigate to **Virtual Services** > **View/Modify Services**
2. Select **modify** on your main Virtual Service
3. Open the **SubVSs** dropdown
4. You'll see your new SubVS at the bottom with a **red highlight** over the empty rule. Select this.
5. Find your rule from the dropdown, and click **add** then **<-back**

## Configuration

Create a `.env` file in the project root with the following variables. Use `.env.example` as a template.

### Kemp Configuration

Before configuring the environment variables, you need to enable API access on your Kemp LoadMaster:

1. Log into your Kemp LoadMaster WebUI
2. Navigate to **Certificates & Security** > **Remote Access**
3. Check the **Enable API Interface** box
4. Leave the port field **blank**

Now configure the following environment variables:

**KEMP_API_KEY**
- Location: **System Configuration** > **User Management**
- Click **Generate New APIKey**
- Copy the generated key

**KEMP_VS_IP**
- Location: **Virtual Services** > **View/Modify Services**
- Copy the blue IP address on the top left (your main Virtual Service)
- Do NOT include the port number (e.g., use `192.168.1.101`, not `192.168.1.101:443`)

**KEMP_URL**
- The full URL of your Kemp LoadMaster WebUI
- Example: `https://192.168.1.100`

### Cloudflare Configuration

**CF_API_KEY**

To create a Cloudflare API token:

1. Log into Cloudflare and go to **Profile** (top right corner)
2. Select **API Tokens**
3. Click **Create Token**
4. Select **Create Custom Token**
5. Configure the token:
   - **Token name**: Kemp-SubVS-Launch
   - **Permissions**:
     - Zone > DNS > Edit
   - **Zone Resources**: Include > Specific zone > [Select your zone]
   - **Client IP Address Filtering**: Leave blank
   - **TTL**: Leave blank
6. Click **Continue to summary**
7. Click **Create Token**
8. Copy the token and use it as your `CF_API_KEY`

**CF_ZONE_ID**

Your Cloudflare Zone ID can be found:
- Log into Cloudflare
- Select your domain
- Scroll down on the **Overview** page
- Copy the **Zone ID** from the right sidebar

For more details, see: https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids/#copy-your-zone-id

**PUB_IP**

Your public IPv4 address. Find it here: https://whatismyipaddress.com/

## Usage

Run the application:
```bash
uv run python main.py
```

### Example

```
> uv run python main.py

Enter a name for the App (alpha-numeric): MyApp
Enter the full domain for the App (ex: app_name.example.com): myapp.example.com
Enter the IP address where the app is hosted (ex: 192.168.1.100): 192.168.1.50
Enter the port number (ex: 443 or 8443): 8443
Create DNS entry for this app? (y/n): y

=========================================
Creating App with the following details:
Name: MyApp
Domain: myapp.example.com
Real Server: 192.168.1.50
Real Port: 8443
Create DNS Entry: y
=========================================

Proceed? (y/n): y

Rule added successfully.
SubVS added successfully with ID: 12
SubVS Name and HTTP check method updated successfully.
Real server added successfully.
Successfully created DNS record for myapp.example.com

App created successfully.
Remember to link the rule to the new SubVS manually in the WebUI!
```

## Troubleshooting

**API Connection Errors**
- Verify the Kemp API is enabled
- Check that `KEMP_URL` is correct and accessible
- Ensure SSL certificate warnings are not blocking requests

**Invalid Credentials**
- Regenerate the API key in Kemp
- Verify the API key is correctly copied to `.env`

**DNS Creation Fails**
- Verify Cloudflare API token has DNS Edit permissions
- Check that the Zone ID is correct
- Ensure the domain matches the zone in Cloudflare

**Real Server Not Responding**
- Verify the backend server IP and port are correct
- Check firewall rules allow traffic from the Kemp LoadMaster
- Ensure the backend service is running

## Installation & Setup

### First Time Setup with uv

If you don't have [uv](https://docs.astral.sh/uv/) installed yet, follow these steps:

1. **Install uv**
   - Visit: https://docs.astral.sh/uv/getting-started/installation/
   - Follow the installation instructions for your operating system

2. **Set up Python and dependencies**:
   
   In the project folder, right-click and launch "open in terminal", then run:
   ```bash
   uv python install 3.12
   uv sync
   ```

3. **Run the application**:
   ```bash
   uv run python main.py
   ```

## Support

Need help? Submit a ticket on our community Discord:

[![Discord](https://img.shields.io/badge/Discord-%237289DA.svg?logo=discord&logoColor=white)](https://discord.fallenservers.com)