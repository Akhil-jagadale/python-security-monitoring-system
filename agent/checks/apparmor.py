import subprocess
from agent.checks.cis_checks import make_result


def check_apparmor():
    check_id = "CIS-APPARMOR"
    check_name = "AppArmor enabled"

    try:
        output = subprocess.check_output("aa-status", shell=True, text=True)

        if "profiles are in enforce mode" in output:
            return make_result(check_id, check_name, "PASS", "AppArmor enforce mode detected")
        else:
            return make_result(check_id, check_name, "FAIL", "AppArmor not enforcing")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"aa-status failed: {str(e)}")
