"""
evidence.py
===========
Evidence inventory for an oncology asset at Phase III completion.

Author: Siva Annapareddy
Domain: Market Access and Pricing Analytics
"""

from dataclasses import dataclass


@dataclass
class EvidenceItem:
    code:    str
    status:  str
    quality: float
    notes:   str = ""


STATUS_SCORE = {
    "available":   1.00,
    "partial":     0.50,
    "planned":     0.25,
    "unavailable": 0.00,
}


def build_sample_evidence() -> dict:
    return {
        "C1": EvidenceItem("C1", "available", 0.95,
            "Phase III APEX trial vs SOC — fully powered pre-specified endpoints"),
        "C2": EvidenceItem("C2", "partial", 0.70,
            "OS data immature at data cut. PFS data mature and significant."),
        "C3": EvidenceItem("C3", "available", 0.90,
            "EQ-5D-5L collected at all timepoints. Mapped to 3L for UK tariff."),
        "C4": EvidenceItem("C4", "available", 0.85,
            "Pre-specified subgroup analyses by line of therapy available in CSR."),
        "C5": EvidenceItem("C5", "partial", 0.60,
            "NMA in progress. Two indirect treatment nodes missing."),
        "C6": EvidenceItem("C6", "unavailable", 0.00,
            "Long-term extension study not yet initiated."),
        "C7": EvidenceItem("C7", "available", 0.80,
            "FACT-G patient-reported outcomes. Significant improvement vs comparator."),
        "E1": EvidenceItem("E1", "available", 0.88,
            "UK cost-effectiveness model complete. Base case ICER GBP 24500 per QALY."),
        "E2": EvidenceItem("E2", "available", 0.85,
            "NHS budget impact model at 5-year horizon complete. Validated by health economist."),
        "E3": EvidenceItem("E3", "available", 0.90,
            "PSA with 10000 iterations complete. 95th percentile ICER GBP 31200 per QALY."),
        "E4": EvidenceItem("E4", "available", 0.92,
            "EQ-5D UK tariff values applied throughout model."),
        "E5": EvidenceItem("E5", "unavailable", 0.00,
            "Productivity loss not modelled. Excluded from base case."),
        "R1": EvidenceItem("R1", "partial", 0.55,
            "SACT database analysis planned. UK Biobank linkage in scoping phase."),
        "R2": EvidenceItem("R2", "unavailable", 0.00,
            "Real-world comparator outcomes study not started."),
        "EP1": EvidenceItem("EP1", "available", 0.90,
            "CRUK incidence and prevalence data. Cancer Research UK 2024 statistics."),
        "EP2": EvidenceItem("EP2", "available", 0.95,
            "Unmet need documented from NICE scope letter."),
    }


if __name__ == "__main__":
    evidence = build_sample_evidence()
    print(f"Total evidence items: {len(evidence)}")
    print()
    by_status = {}
    for code, item in evidence.items():
        by_status.setdefault(item.status, []).append(code)
    for status, codes in sorted(by_status.items()):
        print(f"{status:12s}: {', '.join(codes)}")