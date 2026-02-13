def make_result(check_id, check_name, status, evidence):
    return {
        "check_id": check_id,
        "check_name": check_name,
        "status": status,
        "evidence": evidence
    }
