"""
NetSage AI - Run AI diagnosis over all cases in data/cases.csv
Reads the prompt template, fills in each case, calls the Claude API,
and saves the parsed JSON response to results/ai_results.csv.

Requires: pip install anthropic pandas
Requires an ANTHROPIC_API_KEY environment variable to be set.
"""

import csv
import json
import os
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

PROMPT_TEMPLATE_PATH = "prompts/diagnose_prompt.md"
CASES_PATH = "data/cases.csv"
OUTPUT_PATH = "results/ai_results.csv"


def load_prompt_template():
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(template, case):
    return template.replace("{symptom}", case["symptom"]) \
                    .replace("{topology_note}", case["topology_note"]) \
                    .replace("{show_output}", case["show_output"])


def diagnose_case(template, case):
    prompt = build_prompt(template, case)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    # Strip markdown fences if the model adds them despite instructions
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"root_cause": "PARSE_ERROR", "raw_response": text}


def main():
    template = load_prompt_template()
    os.makedirs("results", exist_ok=True)

    with open(CASES_PATH, newline="", encoding="utf-8") as f:
        cases = list(csv.DictReader(f))

    rows = []
    for case in cases:
        print(f"Diagnosing case {case['case_id']}...")
        result = diagnose_case(template, case)
        rows.append({
            "case_id": case["case_id"],
            "expected_fault": case["expected_fault"],
            "ai_root_cause": result.get("root_cause", ""),
            "ai_osi_layer": result.get("osi_layer", ""),
            "ai_confidence": result.get("confidence", ""),
            "ai_evidence": result.get("evidence", ""),
            "ai_next_command": result.get("next_command", ""),
            "ai_fix_steps": " | ".join(result.get("fix_steps", [])) if isinstance(result.get("fix_steps"), list) else result.get("fix_steps", ""),
        })

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
