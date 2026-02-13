import platform
import subprocess


def run_command(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, text=True).strip()
        return result
    except Exception:
        return ""


def collect_host_info():
    hostname = run_command("hostname")
    kernel = run_command("uname -r")

    os_name = run_command("lsb_release -d -s")
    if not os_name:
        os_name = platform.system()

    ip_address = run_command("hostname -I").split()
    ip = ip_address[0] if len(ip_address) > 0 else "unknown"

    return {
        "hostname": hostname,
        "os": os_name,
        "kernel": kernel,
        "ip_address": ip
    }
