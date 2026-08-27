"""
NetSage AI - Dashboard
Summarizes issue types and AI-vs-human agreement rate from the review log.
Requires: pip install pandas matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt

CASES_PATH = "data/cases.csv"
REVIEW_PATH = "review/human_review_log.csv"


def main():
    cases = pd.read_csv(CASES_PATH)
    review = pd.read_csv(REVIEW_PATH)

    print("=== Cases by concept tag ===")
    print(cases["concept_tag"].value_counts())

    print("\n=== Cases by severity ===")
    print(cases["severity"].value_counts())

    if review["reviewer_decision"].notna().any():
        print("\n=== Reviewer decisions ===")
        counts = review["reviewer_decision"].value_counts()
        print(counts)

        agreement_rate = (review["reviewer_decision"] == "Accepted").mean()
        print(f"\nAI agreement rate: {agreement_rate:.0%}")

        counts.plot(kind="bar", title="AI vs Human Review Outcomes")
        plt.ylabel("Number of cases")
        plt.tight_layout()
        plt.savefig("dashboard/review_summary.png")
        print("Saved chart to dashboard/review_summary.png")
    else:
        print("\nNo reviewer decisions logged yet — fill in review/human_review_log.csv first.")


if __name__ == "__main__":
    main()
