from agent.checks.cis_checks import make_result


def check_password_complexity():
    check_id = "CIS-PASS-COMPLEX"
    check_name = "Password complexity policy enabled"

    try:
        with open("/etc/pam.d/common-password", "r") as f:
            content = f.read()

        if "pam_pwquality.so" in content or "pam_cracklib.so" in content:
            return make_result(check_id, check_name, "PASS", "Password complexity module found")
        else:
            return make_result(check_id, check_name, "FAIL", "No pwquality/cracklib module found")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"Error reading PAM config: {str(e)}")
