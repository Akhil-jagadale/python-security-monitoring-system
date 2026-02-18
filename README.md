# 🛡️ Python Linux Security Monitoring System (CIS Compliance Agent)

A lightweight Linux Security Monitoring Agent built in Python, designed to collect host metadata, installed package inventory, and run CIS Benchmark security checks on Ubuntu Linux systems.

The agent sends security scan results to an AWS serverless backend using **API Gateway + Lambda + DynamoDB**, and the results are displayed on a modern HTML dashboard.

---

## 📌 Features

✅ Collects host details (hostname, OS, kernel, IP)  
✅ Collects installed packages (dpkg-query)  
✅ Runs 10 CIS Benchmark compliance checks  
✅ Generates structured JSON report  
✅ Sends data securely to AWS API Gateway  
✅ Stores results in DynamoDB  
✅ Dashboard to view compliance score, evidence, packages  
✅ Supports automation using systemd timer/service  

---

## 🏗️ Architecture

```

┌───────────────────────────┐
│     Linux Agent (Python)  │
│ - Collect Host Info       │
│ - Collect Packages        │
│ - Run CIS Checks          │
│ - Send JSON Report        │
└─────────────┬─────────────┘
              │ HTTPS POST /ingest
              ▼
┌───────────────────────────┐
│        API Gateway        │
│      POST /ingest         │
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│     Lambda Ingest API     │
│ - Parse JSON report       │
│ - Store into DynamoDB     │
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│         DynamoDB          │
│ Table: LinuxAgentReports  │
│ PK: hostname              │
│ SK: timestamp             │
└─────────────┬─────────────┘
              ▼
              │ Query latest / scan hosts
┌─────────────┴─────────────┐
│       Lambda Query API    │
│ - GET /hosts              │
│ - GET /latest?hostname=X  │
└─────────────┬─────────────┘
              ▼
              │ HTTPS GET requests
┌─────────────┴─────────────┐
│        API Gateway        │
│   GET /hosts, GET /latest │
└─────────────┬─────────────┘
              ▼
              │ Fetch JSON
┌─────────────┴─────────────┐
│   Web Dashboard (HTML)    │ 
│ - Host dropdown           │
│ - CIS compliance score    │
│ - Packages + evidence     │
└───────────────────────────┘


```

---

## 📂 Project Structure

```

python-security-monitoring-system/
├── agent/
│   ├── main.py
│   ├── collector/
│   │   ├── host.py
│   │   └── packages.py
│   ├── checks/
│   │   ├── ssh_root.py
│   │   ├── firewall.py
│   │   ├── time_sync.py
│   │   ├── auditd.py
│   │   ├── apparmor.py
│   │   ├── password_expiry.py
│   │   ├── password_complexity.py
│   │   ├── world_writable.py
│   │   ├── cramfs.py
│   │   ├── gdm_autologin.py
│   │   └── all_checks.py
│   ├── sender/
│   │   └── aws_sender.py
│   └── models/
│       └── report.py
├── frontend/
│   └── index.html
├── requirements.txt
└── README.md

````

---

## 🔒 CIS Benchmark Checks Implemented (10)

This agent implements **10 CIS Ubuntu Linux Level 1 style checks**:

1. SSH Root Login Disabled  
2. Firewall Enabled (UFW)  
3. Time Synchronization Configured (chrony)  
4. Auditd Service Running  
5. AppArmor Enabled  
6. Password Expiry Policy Enforced  
7. Password Complexity Policy Enabled  
8. No World Writable Files in /tmp  
9. cramfs Filesystem Disabled  
10. GDM Auto-login Disabled  

Each check returns:

- `check_id`
- `check_name`
- `status` (PASS/FAIL)
- `evidence`

---

## ☁️ AWS Backend

### AWS Services Used

- API Gateway  
- AWS Lambda  
- DynamoDB  

---

### DynamoDB Table

**Table Name:** `LinuxAgentReports`

**Partition Key:**  
- `hostname`

**Sort Key:**  
- `timestamp`

---

### API Gateway Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/ingest` | Store report from agent |
| GET | `/hosts` | List all monitored hostnames |
| GET | `/latest?hostname=X` | Fetch latest report for a host |

---

## 🚀 Setup & Installation (Ubuntu 22.04)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Akhil-jagadale/security-monitoring-system.git
cd python-security-monitoring-system
````

---

### 2️⃣ Create Virtual Environment (Required on Ubuntu)

Ubuntu uses **PEP 668**, so installing with pip globally is restricted. Use a virtual environment:

```bash
sudo apt update -y
sudo apt install python3-venv -y

python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Agent (with root privileges)

Some CIS checks require root access.

```bash
sudo venv/bin/python -m agent.main
```

---

## 📦 Sample Output

```
...Starting Python Linux Security Agent...
========================================
📊 Collecting host information...
📦 Collecting installed packages...
🔒 Running CIS security checks...
   Score: 6/10 checks passed
☁️  Sending report to AWS...
   ✓ Report successfully sent to AWS!
========================================
✅ Agent execution completed
```

---

## 🌐 Frontend Dashboard

The frontend dashboard fetches data from API Gateway:

* Loads hostnames from `/hosts`
* Fetches latest report using `/latest?hostname=...`

Displays:

* host information
* CIS score
* PASS/FAIL evidence
* installed packages

---

### Run Frontend Locally

```bash
cd frontend
python3 -m http.server 8080
```

Open:

```
http://localhost:8080
```

---

## ⚙️ Automation Using systemd (Optional but Recommended)

To run the agent automatically after reboot and every hour, create:

### `/etc/systemd/system/linux-agent.service`

```ini
[Unit]
Description=Python Linux Security Monitoring Agent
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/ubuntu/python-security-monitoring-system/agent/main.py
User=root
Restart=no

[Install]
WantedBy=multi-user.target
```

---

### `/etc/systemd/system/linux-agent.timer`

```ini
[Unit]
Description=Run Python Linux Agent after boot and every 1 hour

[Timer]
OnBootSec=10sec
OnUnitActiveSec=1h
Unit=linux-agent.service
Persistent=true

[Install]
WantedBy=timers.target
```

---

### Enable Timer

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now linux-agent.timer
```

---

### Verify Timer

```bash
sudo systemctl list-timers --all | grep linux-agent
```

---

### Check Logs

```bash
sudo journalctl -u linux-agent.service -n 50 --no-pager
```

---

## 🧠 Design Decisions

### Why Python?

* Faster development
* Easy system command integration using subprocess
* Simple JSON handling
* Useful for prototyping and automation

---

### Why CIS Benchmark?

CIS benchmarks are widely used in real-world environments for hardening Linux systems and ensuring compliance.

---

### Why DynamoDB?

* Serverless, scalable storage
* Easy to query latest report per host using sort key timestamp

---

## ⚡ Challenges Faced

* API Gateway configuration issues (Missing Authentication Token)
* Lambda parsing issues (KeyError: body)
* Python dependency installation restrictions (PEP 668)
* Running privileged checks requiring root
* Ensuring timer-based automation works after reboot

---

## 🔮 Future Improvements

* Add authentication to API Gateway (API Key or IAM)
* Add more CIS checks (Ubuntu Level 2)
* Add historical report viewing (not only latest)
* Add CloudWatch monitoring & alerting
* Encrypt report data at rest
* Create a proper UI with graphs and trends
* Support multiple Linux distros (rpm/apk support)

---

## 👨‍💻 Author

**Akhilesh Jagadale**

GitHub: [https://github.com/Akhil-jagadale](https://github.com/Akhil-jagadale)
LinkedIn: [https://www.linkedin.com/in/akhileshjagadale/](https://www.linkedin.com/in/akhileshjagadale/)

---
If you want, I can also make a **more premium looking README** with badges (Python, AWS, Linux, CIS, DynamoDB), screenshots section, and demo GIF section.
```
