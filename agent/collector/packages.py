import subprocess


def collect_packages(limit=200):
    packages = []

    try:
        output = subprocess.check_output(
            "dpkg-query -W -f='${binary:Package} ${Version}\n'",
            shell=True,
            text=True
        )

        lines = output.splitlines()

        for line in lines[:limit]:
            parts = line.split()
            if len(parts) >= 2:
                packages.append({
                    "name": parts[0],
                    "version": parts[1]
                })

    except Exception:
        pass

    return packages
