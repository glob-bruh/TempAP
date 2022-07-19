
#!/bin/python3

import os, json, random, sys

print("""
███████████████████████████████████████████            
 ██████████████████████████████████████████            
                                       ███             
 ▒▒▒ ▒▒▒ ▒▒▒▒▒ ▒▒▒ ▒▒▒ ▒▒▒            ███              
  ▒  ▒   ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒ ▒           ███               
  ▒  ▒▒  ▒   ▒ ▒▒▒ ▒▒▒ ▒▒▒          ███                
  ▒  ▒   ▒   ▒ ▒   ▒ ▒ ▒           ███                 
  ▒  ▒▒▒ ▒   ▒ ▒   ▒ ▒ ▒          ████████████████████ 
  zzzzzzzzzzzzzzzzzzzzzzzz       ██████████████████████

Linux-Router Wrapper For Remote SSH Over WiFi.
""")

def jsonConfigLoad():
    with open('config.json', 'r') as configFile:
        try:
            return json.load(configFile)
        except:
            exit("[!] WARNING: Malformed config file. Check config.json. Exiting.")

if len(sys.argv) >= 2:
    argVariable = sys.argv[1]
else:
    argVariable = "run"

if argVariable == "help":
    print("""=====
HELP:
=====

Usage: sudo python3 TempAP.py [argument]

(no argument) - Run script normally and start AP. 
         stop - Stop the AP. 
        setup - Run setup wizard.
         help - Show this menu.
""")
    exit()

if os.geteuid() != 0:
    exit("[!] WARNING: You need to run this script as root. Exiting.")

if argVariable == "stop":
    if os.path.exists("/tmp/TempAPrunning"):
        print("[*] Check and load config.json...")
        configJson = jsonConfigLoad()
        print("[*] Stopping the AP...")
        os.system(f"./lnxrouter --stop {configJson.get('wifiInterface')}")
        os.remove("/tmp/TempAPrunning") 
        exit("[*] AP has been stopped!")
    else:
        exit("[!] AP is not running. Exiting...")

if argVariable == "setup":
    print(f"""======
SETUP:
======

This wizard will prepare the script for use and
generate a config.json file for you based off what you enter.
Please answer the questions below:

---
""")
    askForScriptDown = input("Would you like to download the Linux-router script? [N/y]: ")
    if askForScriptDown == "y" or askForScriptDown == "Y":
        print(f"\n")
        os.system("curl https://raw.githubusercontent.com/garywill/linux-router/master/lnxrouter > lnxrouter && chmod +x lnxrouter")
        askForScriptDep = input(f"\n---\n\nWould you like to also install its dependencies through APT? [N/y]: ")
        if askForScriptDep == "y" or askForScriptDep == "Y":
            print(f"\n")
            listOfDeps = ["procps", "dnsmasq", "iptables", "hostapd", "iw", "haveged"]
            for name in listOfDeps:
                os.system(f"apt install {name} -y")
    print(f"\n---\n")
    os.system("ip a | grep ': '")
    wifiInterface = input(f"\nThe name of the interface you will be hosting the AP from: ")
    print(f"""
---

Do you want to enable relay mode?
Relay mode will take a current network connection and repeat it over the interface you specified from the last question.
""")
    relayMode = input(f"\nEnable relay mode [N/y]: ")
    if relayMode == "y" or relayMode == "Y":
        relayMode = "true"
        relayInterface = input(f"\nThe name of the interface that has the network connection and will be shared with the AP: ")
    else:
        relayMode = "false"
        relayInterface = "none"
    print(f"""
---

Your config.json file will be created. 
If you wish, you can avoid using randomized values by adding your own parameters to the config file. Refer to the README for available parameters.
""")
    input("Press ENTER to continue...")
    setupConfigFile = open("config.json", "w")
    setupConfigFile.write(f"""{{
    "wifiInterface": "{wifiInterface}",
    "relayMode": {relayMode},
    "relayInterface": "{relayInterface}"
}}""")
    setupConfigFile.close()
    print(f"\nDone! Re-run this script as root without the 'setup' argument.")
    exit()

if os.path.exists("/tmp/TempAPrunning"):
    exit("[!] The AP is already running. Exiting...")

print("[*] Check and load config.json...")
if os.path.isfile('config.json') == False:
    exit("[!] WARNING: No config.json file found. Try running with the 'setup' argument to create one. Exiting.")

configJson = jsonConfigLoad()
print("[*] config.json loaded.")

print("[*] Parse JSON...")
if configJson.get('wifiInterface') == None:
    exit("[!] WARNING: You must have a WiFi interface specified in config.json. Exiting.\n")
if configJson.get('relayMode') == None:
    exit("[!] WARNING: You must specify whether relay mode should be on or off. Exiting.\n")
if configJson['relayMode'] == True and configJson.get('relayInterface') == None:
    exit("[!] WARNING: When using relay mode you need to specify a relay interface. Exiting.\n")
if configJson.get('wifiName') == None:
    configJson['wifiName'] = f"Network{random.randint(100,999)}"
    print(f"[*] Network name auto generated: {configJson['wifiName']}")
if configJson.get('apPass') == None:
    configJson['apPass'] = str(random.randint(10000000,99999999))
    print(f"[*] WiFi password auto generated: {configJson['apPass']}")
if configJson.get('gatewayIP') == None:
    configJson['gatewayIP'] = '192.168.0.1'
if configJson.get('macAddress') == None:
    autoMac = ""
    for macLoop in range(0,6):
        autoMac += f"{random.randint(10,99)}:"
        macLoop += 1
    configJson['macAddress'] = autoMac[:-1]
if configJson.get('noVirt') == None:
    configJson['noVirt'] = False

wifiInterface = configJson['wifiInterface']
relayMode = configJson['relayMode']
if relayMode == True:
    relayInterface = configJson['relayInterface']
wifiName = configJson['wifiName']
apPass = configJson['apPass']
gatewayIP = configJson['gatewayIP']
macAddress = configJson['macAddress']
noVirt = configJson['noVirt']

print(f"\n[*] Enable SSH service...")
os.system("service ssh start ; service ssh status | head -n 3")

print(f"\n[*] Start AP...")
print(f"""
=========================
WIFI NAME: {wifiName}

PASSWORD: {apPass[0]}*****{apPass[-1]}

GATEWAY: {gatewayIP}

INTERFACE: {wifiInterface}

MAC: {macAddress}

NOVIRT: {noVirt}
""")

if relayMode == True:
    print(f"RELAY MODE: Enabled\n{relayInterface} -> {wifiInterface}/{wifiName}")
else:
    print("RELAY MODE: Disabled")

print("=========================\n")

if relayMode == True:
    if noVirt  == True:
        os.system(f"./lnxrouter --daemon -w 2 -p {apPass} --mac {macAddress} -g {gatewayIP} -o {relayInterface} --no-virt --ap {wifiInterface} {wifiName}")
    else:
        os.system(f"./lnxrouter --daemon -w 2 -p {apPass} --mac {macAddress} -g {gatewayIP} -o {relayInterface} --ap {wifiInterface} {wifiName}")
else:
    if noVirt  == True:
        os.system(f"./lnxrouter --daemon -w 2 -p {apPass} --mac {macAddress} -g {gatewayIP} --no-virt --ap {wifiInterface} {wifiName}")
    else:
        os.system(f"./lnxrouter --daemon -w 2 -p {apPass} --mac {macAddress} -g {gatewayIP} --ap {wifiInterface} {wifiName}")

os.system("touch /tmp/TempAPrunning")
print(f"\n[*] TO STOP THE AP: Run the script again with the 'stop' argument.")