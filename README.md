# NetSage AI

An AI-assisted troubleshooting helper for Cisco-style Packet Tracer lab issues, with mandatory human review before any diagnosis is accepted.

## Problem
Junior network engineers know individual commands but struggle to connect a symptom to a root cause (VLAN, routing, DHCP, DNS, ACL, or NAT?). NetSage AI takes symptoms, topology notes, and show-command output, and recommends a likely fault, OSI layer, next command, and evidence-backed fix — always reviewed by a human before it's trusted.

## Project structure
```
netsage-ai/
├── data/cases.csv              # 30+ troubleshooting cases
├── prompts/diagnose_prompt.md  # structured AI prompt (forces JSON output)
├── checker/rule_checker.py     # deterministic Python checks (no AI)
├── results/ai_results.csv      # AI diagnosis output per case
├── review/human_review_log.csv # Accepted / Edited / Rejected + notes
├── dashboard/dashboard.py      # summary counts + AI agreement rate
├── demo/                       # demo video or link
└── README.md
```

## How to run

### 1. Install dependencies
```cmd
pip install -r requirements.txt
```

### 2. Run the rule checker
```cmd
python checker\rule_checker.py
```

### 3. Run AI diagnosis on all cases
```cmd
python run_diagnosis.py
```
(Feeds each row of `data\cases.csv` into `prompts\diagnose_prompt.md`, saves output to `results\ai_results.csv`.)

### 4. Review results
Open `review\human_review_log.csv`, mark each case Accepted / Edited / Rejected, and log why for any AI mistakes.

### 5. View the dashboard
```cmd
python dashboard\dashboard.py
```

## Responsible AI
At least 5 cases where the AI's diagnosis was corrected by a human reviewer are logged in `review/human_review_log.csv`, with an explanation of what the AI got wrong.

## Demo
[Link to demo video or see demo/demo.mp4] — shows one broken lab case being diagnosed by AI, reviewed by a human, fixed, and verified.

## Team
- [Name 1]
- [Name 2]
- [Name 3]
