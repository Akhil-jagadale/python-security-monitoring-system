import subprocess
from agent.checks.cis_checks import make_result


def check_auditd():
    check_id = "CIS-AUDITD"
    check_name = "Auditd service running"

    try:
        output = subprocess.check_output("systemctl is-active auditd", shell=True, text=True).strip()

        if output == "active":
            return make_result(check_id, check_name, "PASS", "auditd is active")
        else:
            return make_result(check_id, check_name, "FAIL", f"auditd status: {output}")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"auditd check failed: {str(e)}")
