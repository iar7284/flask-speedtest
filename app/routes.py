
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
import re

# Create blueprint
main = Blueprint('main', __name__)

def get_wifi_name():
    try:
        # Get WiFi info using netsh command
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces']).decode('utf-8')
        # Find SSID in the output
        ssid = re.search(r"SSID\s+: (.*)\r", output)
        if ssid:
            return ssid.group(1)
        return "Not connected to WiFi"
    except:
        return "Unable to get WiFi information"

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