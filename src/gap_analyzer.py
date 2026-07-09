"""
gap_analyzer.py
===============
HTA gap analysis scoring engine.

Matches sponsor evidence inventory against HTA requirement matrices.
Flags mandatory gaps as CRITICAL and scores readiness per market.

SCORING FORMULA
---------------
weighted_score = status_score x quality x requirement_weight

mandatory_score = sum(weighted scores for mandatory reqs only)
                / sum(weights for mandatory reqs only) x 100

RAG LOGIC
---------
GREEN : 0 critical gaps AND mandatory score >= 80%
AMBER : <= 2 critical gaps AND mandatory score >= 60%
RED   : > 2 critical gaps OR mandatory score < 60%

Author: Siva Annapareddy
Domain: Market Access and Pricing Analytics
"""

import pandas as pd
from typing import Dict, List
from src.hta_requirements import HTARequirement
from src.evidence import EvidenceItem, STATUS_SCORE


class HTAGapAnalyzer:
    """
    Scores an evidence inventory against an HTA requirement matrix.
    Identifies gaps, flags critical ones, and computes readiness scores.
    """

    def score_submission(
        self,
        requirements: List[HTARequirement],
        evidence: Dict[str, EvidenceItem]
    ) -> pd.DataFrame:
        """
        For each requirement check if evidence exists and score it.

        Returns a DataFrame with one row per requirement showing
        status, quality, weighted score, and criticality flag.
        """
        rows = []
        for req in requirements:
            ev = evidence.get(req.code)

            if ev is None:
                status, quality, notes = "unavailable", 0.0, "Not in evidence inventory"
            else:
                status, quality, notes = ev.status, ev.quality, ev.notes

            base_score = STATUS_SCORE.get(status, 0.0)
            quality_adjusted = base_score * quality
            weighted_score = quality_adjusted * req.weight

            # CRITICAL = mandatory requirement that is missing or partial
            is_critical = req.mandatory and status in ("unavailable", "partial")
            criticality = "CRITICAL" if is_critical else (
                "SUPPORTIVE GAP" if status == "unavailable" else "OK"
            )

            rows.append({
                "code":           req.code,
                "domain":         req.domain,
                "description":    req.description,
                "mandatory":      req.mandatory,
                "weight":         req.weight,
                "status":         status,
                "quality":        quality,
                "weighted_score": round(weighted_score, 3),
                "critical":       is_critical,
                "criticality":    criticality,
                "notes":          notes,
            })

        return pd.DataFrame(rows)

    def readiness_score(self, df: pd.DataFrame) -> dict:
        """
        Compute overall, mandatory-only, and domain-level readiness scores.

        The mandatory_score is the primary go/no-go metric.
        A high overall score with low mandatory score means
        supportive evidence is strong but required evidence is weak.
        That is still a submission risk.
        """
        scores = {}

        # Domain-level scores
        for domain in df["domain"].unique():
            sub = df[df["domain"] == domain]
            max_possible = sub["weight"].sum()
            achieved = sub["weighted_score"].sum()
            scores[f"{domain}_score"] = round(
                achieved / max_possible * 100, 1
            ) if max_possible > 0 else 0.0

        # Overall score across all requirements
        overall_max = df["weight"].sum()
        overall_ach = df["weighted_score"].sum()
        scores["overall_score"] = round(
            overall_ach / overall_max * 100, 1
        ) if overall_max > 0 else 0.0

        # Mandatory-only score — primary decision metric
        mandatory = df[df["mandatory"]]
        mand_max = mandatory["weight"].sum()
        mand_ach = mandatory["weighted_score"].sum()
        scores["mandatory_score"] = round(
            mand_ach / mand_max * 100, 1
        ) if mand_max > 0 else 0.0

        scores["critical_gaps"] = int(df["critical"].sum())
        scores["total_gaps"] = int((df["status"] == "unavailable").sum())

        return scores

    def rag_status(self, mandatory_score: float, critical_gaps: int) -> str:
        """
        RAG status based on mandatory score and critical gap count.

        GREEN : Ready to submit
        AMBER : Conditional — gaps need closure plan
        RED   : Not ready — submission would likely fail
        """
        if critical_gaps == 0 and mandatory_score >= 80:
            return "GREEN"
        elif critical_gaps <= 2 and mandatory_score >= 60:
            return "AMBER"
        else:
            return "RED"


if __name__ == "__main__":
    from src.hta_requirements import HTA_BODIES
    from src.evidence import build_sample_evidence

    evidence = build_sample_evidence()
    analyzer = HTAGapAnalyzer()

    for body, requirements in HTA_BODIES.items():
        df = analyzer.score_submission(requirements, evidence)
        scores = analyzer.readiness_score(df)
        rag = analyzer.rag_status(scores["mandatory_score"], scores["critical_gaps"])

        print(f"\n{body}")
        print(f"  Overall score:    {scores['overall_score']}%")
        print(f"  Mandatory score:  {scores['mandatory_score']}%")
        print(f"  Critical gaps:    {scores['critical_gaps']}")
        print(f"  RAG status:       {rag}")

        critical = df[df["critical"]]
        if not critical.empty:
            print(f"  Critical gaps to close:")
            for _, r in critical.iterrows():
                print(f"    [{r['code']}] {r['description']}")
                print(f"         Status: {r['status']} | {r['notes']}")