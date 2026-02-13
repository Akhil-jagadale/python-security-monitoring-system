from agent.checks.cis_checks import make_result


def check_cramfs_disabled():
    check_id = "CIS-CRAMFS"
    check_name = "Unused filesystem cramfs disabled"

    try:
        with open("/etc/modprobe.d/blacklist.conf", "r") as f:
            content = f.read()

        if "cramfs" in content:
            return make_result(check_id, check_name, "PASS", "cramfs is blacklisted")
        else:
            return make_result(check_id, check_name, "FAIL", "cramfs blacklist entry not found")

    except Exception:
        return make_result(check_id, check_name, "FAIL", "blacklist.conf not found or unreadable")
