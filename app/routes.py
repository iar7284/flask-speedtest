
#from flask import Blueprint, render_template, jsonify
#from .speedtest import run_speedtest

#main = Blueprint('main', __name__)

#@main.route('/')
#def index():
#    return render_template('index.html')

#@main.route('/speedtest')
#def speedtest():
#    result = run_speedtest()
#    return jsonify(result)

from flask import Blueprint, jsonify, render_template
import speedtest
import subprocess
import platform
import socket   
import re

# Create blueprint
main = Blueprint('main', __name__)

def get_wifi_name():
    try:
        # For Windows
        if platform.system() == "Windows":
            output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
            if "There is no wireless interface on the system." in output:
                return "No WiFi adapter available"
            
            network_info = {}
            for line in output.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    network_info['ssid'] = line.split(":")[1].strip()
                if "Signal" in line:
                    network_info['signal'] = line.split(":")[1].strip()
            
            return network_info.get('ssid', 'Not connected')
            
        # For Linux (Azure App Service runs on Linux)
        else:
            try:
                hostname = socket.gethostname()
                return f"Server: {hostname}"
            except:
                return "Unable to get network information"
                
    except Exception as e:
        return f"Network detection error: {str(e)}"
    
    #try:
        # Get WiFi info using netsh command
    #    output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
        # Find SSID in the output
    #    ssid = re.search(r"SSID\s+: (.*)\r", output)
    #    if ssid:
    #        return ssid.group(1)
    #    return "Not connected to WiFi"
    #except:
    #    return "Unable to get WiFi information"

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/speedtest')
def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    
    # Get speeds
    download_speed = round(st.download() / 1_000_000, 2)  # Convert to Mbps
    upload_speed = round(st.upload() / 1_000_000, 2)      # Convert to Mbps
    ping = round(st.results.ping, 2)
    
    # Get current WiFi name
    wifi_name = get_wifi_name()
    
    return jsonify({
        'download': download_speed,
        'upload': upload_speed,
        'ping': ping,
        'wifi_name': wifi_name
    })