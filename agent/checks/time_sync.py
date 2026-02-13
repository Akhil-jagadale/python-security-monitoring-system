import subprocess
from agent.checks.cis_checks import make_result


def check_time_sync():
    check_id = "CIS-TIME-SYNC"
    check_name = "Time synchronization configured (chrony)"

    try:
        output = subprocess.check_output("systemctl is-active chrony", shell=True, text=True).strip()

        if output == "active":
            return make_result(check_id, check_name, "PASS", "chrony service is active")
        else:
            return make_result(check_id, check_name, "FAIL", f"chrony service status: {output}")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"chrony check failed: {str(e)}")
