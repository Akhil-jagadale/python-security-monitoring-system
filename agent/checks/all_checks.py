from agent.checks.ssh_root import check_ssh_root_login
from agent.checks.firewall import check_firewall_ufw
from agent.checks.time_sync import check_time_sync
from agent.checks.auditd import check_auditd
from agent.checks.apparmor import check_apparmor
from agent.checks.password_expiry import check_password_expiry
from agent.checks.password_complexity import check_password_complexity
from agent.checks.world_writable import check_world_writable
from agent.checks.cramfs import check_cramfs_disabled
from agent.checks.gdm_autologin import check_gdm_autologin


def run_all_checks():
    return [
        check_ssh_root_login(),
        check_firewall_ufw(),
        check_time_sync(),
        check_auditd(),
        check_apparmor(),
        check_password_expiry(),
        check_password_complexity(),
        check_world_writable(),
        check_cramfs_disabled(),
        check_gdm_autologin()
    ]
