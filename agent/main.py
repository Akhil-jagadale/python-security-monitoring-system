import datetime
from agent.collector.host import collect_host_info
from agent.collector.packages import collect_packages
from agent.checks.all_checks import run_all_checks
from agent.sender.aws_sender import send_report


def main():
    print("...Starting Python Linux Security Agent...")
    print("========================================")

    print("📊 Collecting host information...")
    host = collect_host_info()
    print(f"   ✓ Hostname: {host['hostname']}")

    print("📦 Collecting installed packages...")
    packages = collect_packages(limit=200)
    print(f"   ✓ Found {len(packages)} packages")

    print("🔒 Running CIS security checks...")
    cis_results = run_all_checks()

    pass_count = len([c for c in cis_results if c["status"] == "PASS"])
    total = len(cis_results)

    print(f"   Score: {pass_count}/{total} checks passed")

    report = {
        "host": host,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "packages": packages,
        "cis_results": cis_results,
        "agent_type": "python"
    }

    print("☁️  Sending report to AWS...")
    success, response = send_report(report)

    if success:
        print("   ✓ Report successfully sent to AWS!")
    else:
        print("   ✗ Failed to send report!")
        print(response)

    print("========================================")
    print("✅ Agent execution completed")


if __name__ == "__main__":
    main()
