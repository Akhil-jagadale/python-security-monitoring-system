from agent.checks.cis_checks import make_result


def check_gdm_autologin():
    check_id = "CIS-GDM-AUTOLOGIN"
    check_name = "GDM auto-login disabled"

    try:
        with open("/etc/gdm3/custom.conf", "r") as f:
            content = f.read()

        if "AutomaticLoginEnable=true" in content:
            return make_result(check_id, check_name, "FAIL", "AutomaticLoginEnable=true found")
        else:
            return make_result(check_id, check_name, "PASS", "Auto-login not enabled")

    except Exception:
        return make_result(check_id, check_name, "PASS", "GDM not installed (custom.conf not found)")
