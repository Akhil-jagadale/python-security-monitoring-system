import subprocess
from agent.checks.cis_checks import make_result


def check_world_writable():
    check_id = "CIS-WORLD-WRITABLE"
    check_name = "No world writable files in /tmp"

    try:
        output = subprocess.check_output("find /tmp -type f -perm -0002 2>/dev/null | head -n 5", shell=True, text=True).strip()

        if output == "":
            return make_result(check_id, check_name, "PASS", "No world-writable files found in /tmp")
        else:
            return make_result(check_id, check_name, "FAIL", f"World writable files found:\n{output}")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"Check failed: {str(e)}")
