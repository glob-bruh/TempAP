
<center>
# TempAP
![logo](logo.png)
</center>

## What is this script?

This python script is simply a wrapper for [Berate-AP](https://github.com/sensepost/berate_ap), a tool designed to deploy rouge wireless access points. The original use case for this script was to be able to access portable Linux computers (like a laptop) over a cell phone via SSH temporarily, but there is other use cases for this, for example, an on-the-fly wireless repeater.

## Setup:

The steps to setup this script are as followed:
1. Install openssh-server and berate-ap. You can figure out how to install these by searching "how to install openssh-server" and "how to install berate-ap".
2. Make sure the TempAP script is downloaded.
3. Run `python3 TempAP.py setup`.
4. Make sure either your config.json file is present or you have generated one.
5. If you are using a laptop you should adjust your power options to avoid the laptop from shutting off or going into hibernation, thus stopping the script. 

## Configuration:

This script requires a file called config.json to be present. The config.json file is a file that holds various parameters. The reason why its a file and not command-line arguments is to allow the same pre-made configuration to be used multiple times "on-the-fly" without any user intervention.

The following is a list of possible configuration parameters that can be used:

- **Required** (the script will not run without these):
  - **wifiInterface (String):** The interface to host the wireless access point from.
  - **relayMode (Boolean):** Whether to enable the repeating of the current WiFi signal from an active connection or not.
  - **relayInterface (String):** If relayMode is set to true, this is the WiFi interface that the active connection is running on. The connection from this interface will be shared over the interface specified in wifiInterface.
- **Not Required** (these will be auto generated if not included):
  - **wifiName (String):** Name/SSID of the wireless access point to broadcast. 
  - **apPass (String):** WPA2 password to use for the broadcasted wireless access point.
  - **gatewayIP (String):** The preferred local IP of the computer broadcasting the wireless access point.
  - **macAddress (String):** MAC address for the wireless access point to broadcast. 
  - **noVirt (Boolean):** *"Do not create virtual interface"*. This can help if there is interface issues when starting the access point.

**<u>Example config.json file:</u>**

```json
{
    "wifiInterface": "wlan1",
    "relayMode": false,
    "relayInterface": "none"
}
````

If you are not able to construct your own configuration file then run the command in step 3 of the Setup section. 

## License:

Licensed under [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
