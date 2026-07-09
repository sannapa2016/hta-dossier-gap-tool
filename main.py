"""
main.py
=======
Single entry point for the HTA Dossier Gap Analysis Tool.

Runs gap analysis for NICE, G-BA, and HAS and exports results.

Author: Siva Annapareddy
Domain: Market Access and Pricing Analytics
"""

import os
import pandas as pd
from src.hta_requirements import HTA_BODIES
from src.evidence import build_sample_evidence
from src.gap_analyzer import HTAGapAnalyzer

os.makedirs("outputs", exist_ok=True)


def main():
    print("=" * 65)
    print("HTA DOSSIER GAP ANALYSIS TOOL")
    print("Author: Siva Annapareddy | Amrak Pharma Analytics")
    print("=" * 65)

    evidence = build_sample_evidence()
    analyzer = HTAGapAnalyzer()
    summary_rows = []

    for body, requirements in HTA_BODIES.items():
        print(f"\n{'=' * 65}")
        print(f"[{body}]")
        print(f"{'=' * 65}\n")

        df = analyzer.score_submission(requirements, evidence)
        scores = analyzer.readiness_score(df)
        rag = analyzer.rag_status(
            scores["mandatory_score"], scores["critical_gaps"]
        )

        # Full requirement breakdown
        print(df[[
            "code", "domain", "mandatory",
            "status", "quality", "weighted_score", "criticality"
        ]].to_string(index=False))

        # Scores
        print(f"\n  Overall readiness:   {scores['overall_score']}%")
        print(f"  Mandatory score:     {scores['mandatory_score']}%")
        print(f"  Critical gaps:       {scores['critical_gaps']}")
        print(f"  Total gaps:          {scores['total_gaps']}")
        print(f"  RAG status:          {rag}")

        # Domain breakdown
        print(f"\n  Domain scores:")
        for key, val in scores.items():
            if key.endswith("_score") and key not in (
                "overall_score", "mandatory_score"
            ):
                domain = key.replace("_score", "")
                print(f"    {domain:<20s}: {val}%")

        # Critical gaps detail
        critical = df[df["critical"]]
        if not critical.empty:
            print(f"\n  CRITICAL GAPS TO CLOSE ({len(critical)}):")
            for _, r in critical.iterrows():
                print(f"    [{r['code']}] {r['description']}")
                print(f"         Status: {r['status']} | Quality: {r['quality']}")
                print(f"         Note:   {r['notes']}")
        else:
            print(f"\n  No critical gaps — evidence package is submission ready")

        # Export per HTA body
        filename = body.split("(")[0].strip().lower().replace(" ", "_")
        df.to_csv(f"outputs/hta_gap_{filename}.csv", index=False)

        summary_rows.append({
            "hta_body":        body,
            "overall_score":   scores["overall_score"],
            "mandatory_score": scores["mandatory_score"],
            "critical_gaps":   scores["critical_gaps"],
            "total_gaps":      scores["total_gaps"],
            "rag_status":      rag,
        })

    # Summary across all HTA bodies
    print(f"\n{'=' * 65}")
    print("[SUMMARY — ALL HTA BODIES]")
    print(f"{'=' * 65}\n")
    summary_df = pd.DataFrame(summary_rows)
    print(summary_df.to_string(index=False))

    # Key insight
    red_markets = summary_df[summary_df["rag_status"] == "RED"]
    amber_markets = summary_df[summary_df["rag_status"] == "AMBER"]
    green_markets = summary_df[summary_df["rag_status"] == "GREEN"]

    print(f"\n  GREEN markets (ready to submit): {len(green_markets)}")
    print(f"  AMBER markets (gaps to close):   {len(amber_markets)}")
    print(f"  RED markets (not ready):         {len(red_markets)}")

    total_critical = summary_df["critical_gaps"].sum()
    print(f"\n  Total critical gaps across all markets: {total_critical}")
    print(f"  Most critical market: "
          f"{summary_df.loc[summary_df['critical_gaps'].idxmax(), 'hta_body']}")

    summary_df.to_csv("outputs/hta_gap_summary.csv", index=False)

    print("\n[OK] Results saved to outputs/")
    print("=" * 65)


if __name__ == "__main__":
    main()