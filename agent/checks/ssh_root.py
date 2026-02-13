from agent.checks.cis_checks import make_result


def check_ssh_root_login():
    check_id = "CIS-SSH-ROOT"
    check_name = "Root login disabled over SSH"

    try:
        with open("/etc/ssh/sshd_config", "r") as f:
            config = f.read()

        if "PermitRootLogin no" in config:
            return make_result(check_id, check_name, "PASS", "PermitRootLogin no found")
        else:
            return make_result(check_id, check_name, "FAIL", "PermitRootLogin no not found")

    except Exception as e:
        return make_result(check_id, check_name, "FAIL", f"Error reading sshd_config: {str(e)}")
