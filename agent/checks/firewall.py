import subprocess
from agent.checks.cis_checks import make_result


def check_firewall_ufw():
    check_id = "CIS-FW-UFW"
    check_name = "Firewall enabled (UFW)"

    try:
        output = subprocess.check_output("ufw status", shell=True, text=True)

        if "Status: active" in output:
            return make_result(check_id, check_name, "PASS", output.strip())
        else:
            return make_result(check_id, check_name, "FAIL", output.strip())

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"ufw not installed or error: {str(e)}")
