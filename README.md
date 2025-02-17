# UltimateSpoofer
A GUI tool for scanning local networks and managing MAC addresses of network devices.

## Requirements
- Windows OS
- Admin privileges
- Active Ethernet connection (Wi-Fi not supported)

## Features
- Scans local network for connected devices
- Displays IP addresses, MAC addresses, and device names
- Save device information for future reference
- Copy MAC addresses to clipboard
- Change your network adapter's MAC address
- Edit device names

## Usage
1. Run the exe with administrator privileges
2. Select your Ethernet adapter from the dropdown menu
3. Click "Start Scan" to discover devices on your network
4. Right-click on devices to:
   - Save device information
   - Copy MAC address
   - Set your adapter's MAC address to match the selected device

## Note
This tool only works with Ethernet connections because it relies on ARP (Address Resolution Protocol) scanning, which is not reliable over Wi-Fi connections. The MAC address changing feature requires a wired Ethernet connection.
