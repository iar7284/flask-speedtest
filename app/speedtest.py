
import speedtest

def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    download = st.download()
    upload = st.upload()
    ping = st.results.ping

    return {
        'download': round(download / 1_000_000, 2),
        'upload': round(upload / 1_000_000, 2),
        'ping': round(ping, 2)
    }
