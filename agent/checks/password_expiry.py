from agent.checks.cis_checks import make_result


def check_password_expiry():
    check_id = "CIS-PASS-EXP"
    check_name = "Password expiration policy enforced"

    try:
        with open("/etc/login.defs", "r") as f:
            content = f.read()

        if "PASS_MAX_DAYS" in content:
            return make_result(check_id, check_name, "PASS", "PASS_MAX_DAYS found in /etc/login.defs")
        else:
            return make_result(check_id, check_name, "FAIL", "PASS_MAX_DAYS not found")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"Error reading login.defs: {str(e)}")
