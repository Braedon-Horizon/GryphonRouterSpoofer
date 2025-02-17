# Network Scanner Tool for Gryphon Parental Controls
A GUI tool for scanning local networks and managing MAC addresses of network devices. Coded Specifically for Gryphon Parental Controls

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

## How to use with Gryphon Parental Controls:
1. Open Command Prompt as NON admin
![HOW TO 1](https://github.com/user-attachments/assets/1f992302-e1ba-4ec7-98be-3ce2c352a0bb)
2. Type in "ipconfig" and press enter
![how to 2](https://github.com/user-attachments/assets/14e9ab3d-bc7a-458b-8a4d-f0066e0fd806)
3. Copy and Paste your Defualt Gateway(Mine have been blurred out)
![How to 3](https://github.com/user-attachments/assets/48e27f37-a7d6-4e16-acd5-ec62649e9176)
4. Enter it into you're browsers search bar and press enter
This is how we will test and name our devices on our network.
5. Open up Network Scanner now.
6. Click Scan Now
![How to 4](https://github.com/user-attachments/assets/371797b8-4675-4248-99bb-9b4fe29b7bb8)
It will take a while to scan ~ 30-60 seconds
It will show a list of devices connected to the network
![How to 5](https://github.com/user-attachments/assets/8fa5e5c6-3792-47ca-a60a-797cd3bbc064)
You will most likley be able to tell a devices name/what it is fom the defualt device name.
8.Right click on a device you think is unaffected by parental controls.( In my case, I can tell by the default name, that this is my TV, and most likely is unaffected by Gryphon)
9."Click on Set MAC Address To This Device", this will set your computer MAC address to the selected devices MAC address. This is effectivly pretending to be that device.
You should get a pop up telling you that it worked
10. click ok.
![6](https://github.com/user-attachments/assets/798aeb42-a394-4bd8-b6b7-c729eb35ef45)
11. Go back to the webpage we setup with our defualt gateway
12. Click on "About This Device" in the top right of the screen.
![7](https://github.com/user-attachments/assets/ae3be20a-ab91-4ff7-8cc8-aa6fa09ce3c5)
If you chose an unrestricted device, it should be unrestriced and unmanaged. If its restricted, try every device until you get an unrestricted device.
13. Copy the "Device Name"
![8](https://github.com/user-attachments/assets/17381882-4563-4388-a48e-cb13e4b0abd8)
14. Back in Our Network Scanner we can doubled click on the name of our device and rename it.
![9](https://github.com/user-attachments/assets/c7451bb5-3f8e-4471-b549-1677fb052e98)
15. Then right click and click "Save Device"
![10](https://github.com/user-attachments/assets/b2f38113-b43e-43c4-942d-57b81ae7431d)

What this does is essentially save the device so you can pretend to be that device whenever you want to. If you want to your original device, find it in the device list and set it as your MAC adress.
Then name it and save it for ease of use.

## God Mode
To find god mode, do the steps 8-15 for every device scanned. Eventually you should find the actual router. It will look like this:
![NOTHIGN](https://github.com/user-attachments/assets/f14db7b9-16e3-473a-9076-a32a5ad2fc3b)
This means that you have found the router. This has no restricitons and as of February 2025, has no limits and cannot be fixed by your parents as far as I know.
Have fun :)

## Contact Me at Sot_Ente on Discord
