"""
hta_requirements.py
===================
HTA requirement matrices for NICE (UK), G-BA (Germany), and HAS (France).

Each HTA body has a different evidence framework:
    NICE  : Cost-effectiveness. Needs ICER below threshold. EQ-5D mandatory.
    G-BA  : Clinical benefit vs appropriate comparator (gAV). No ICER needed.
    HAS   : SMR and ASMR ratings. Comparative clinical data drives negotiation.

Author: Siva Annapareddy
Domain: Market Access and Pricing Analytics
"""

from dataclasses import dataclass
from typing import List


@dataclass
class HTARequirement:
    """
    A single evidence requirement for an HTA submission.

    Attributes
    ----------
    code : str
        Unique identifier matching evidence inventory codes
    domain : str
        clinical | economic | epidemiological | rwe
    description : str
        Plain English description of the requirement
    mandatory : bool
        True = required for submission. Missing = CRITICAL gap.
        False = supportive. Missing = reduces score but not blocking.
    weight : float
        Importance within domain (0.0 to 1.0)
    """
    code:        str
    domain:      str
    description: str
    mandatory:   bool
    weight:      float


def build_nice_requirements() -> List[HTARequirement]:
    """
    NICE Single Technology Appraisal requirement matrix.

    NICE uses cost-effectiveness analysis with an ICER threshold
    of GBP 20,000 to 30,000 per QALY. EQ-5D with UK tariff values
    is mandatory. Mature OS data is critical for reliable economic
    modelling. Budget impact from NHS perspective is required.
    """
    return [
        # Clinical evidence
        HTARequirement("C1", "clinical",
            "Phase III RCT versus appropriate comparator",
            mandatory=True,  weight=1.00),
        HTARequirement("C2", "clinical",
            "Overall survival data (mature)",
            mandatory=True,  weight=0.95),
        HTARequirement("C3", "clinical",
            "Health-related QoL measured with EQ-5D",
            mandatory=True,  weight=0.90),
        HTARequirement("C4", "clinical",
            "Subgroup analyses by line of therapy",
            mandatory=False, weight=0.70),
        HTARequirement("C5", "clinical",
            "Indirect treatment comparison (NMA) if no head-to-head",
            mandatory=False, weight=0.75),
        HTARequirement("C6", "clinical",
            "Long-term extension study data",
            mandatory=False, weight=0.65),
        # Economic evidence
        HTARequirement("E1", "economic",
            "Cost-effectiveness model with ICER vs NICE threshold",
            mandatory=True,  weight=1.00),
        HTARequirement("E2", "economic",
            "Budget impact model from NHS perspective",
            mandatory=True,  weight=0.90),
        HTARequirement("E3", "economic",
            "Probabilistic sensitivity analysis (PSA)",
            mandatory=True,  weight=0.85),
        HTARequirement("E4", "economic",
            "Utility values using EQ-5D UK tariff",
            mandatory=True,  weight=0.90),
        HTARequirement("E5", "economic",
            "Productivity loss and indirect costs",
            mandatory=False, weight=0.50),
        # Real world evidence
        HTARequirement("R1", "rwe",
            "UK-specific epidemiology data",
            mandatory=False, weight=0.70),
        HTARequirement("R2", "rwe",
            "Real-world comparator outcomes",
            mandatory=False, weight=0.75),
        # Epidemiological
        HTARequirement("EP1", "epidemiological",
            "Disease prevalence and incidence in UK",
            mandatory=True,  weight=0.80),
        HTARequirement("EP2", "epidemiological",
            "Unmet need documentation",
            mandatory=True,  weight=0.85),
    ]


def build_gba_requirements() -> List[HTARequirement]:
    """
    G-BA AMNOG benefit assessment requirement matrix.

    G-BA does NOT use cost-effectiveness or ICER.
    It assesses Added Benefit (Zusatznutzen) versus the
    Appropriate Comparator Therapy (gAV — geeignete
    Vergleichstherapie) defined by G-BA before submission.

    Getting the gAV wrong is the most common dossier failure.
    The benefit rating (Major/Considerable/Minor/None) directly
    drives the price negotiation with GKV-Spitzenverband.
    """
    return [
        HTARequirement("C1", "clinical",
            "Phase III RCT versus G-BA defined gAV (appropriate comparator)",
            mandatory=True,  weight=1.00),
        HTARequirement("C2", "clinical",
            "Overall survival as primary or key secondary endpoint",
            mandatory=True,  weight=0.95),
        HTARequirement("C3", "clinical",
            "Morbidity endpoints (response rate, PFS)",
            mandatory=True,  weight=0.85),
        HTARequirement("C4", "clinical",
            "Safety and adverse event comparative data vs gAV",
            mandatory=True,  weight=0.90),
        HTARequirement("C5", "clinical",
            "Health-related QoL — SF-36 for Germany, EQ-5D for EU submissions",
            mandatory=True,  weight=0.85),
        HTARequirement("C6", "clinical",
            "Subgroup data per SmPC approved indication",
            mandatory=False, weight=0.75),
        HTARequirement("C7", "clinical",
            "Patient-reported outcomes",
            mandatory=False, weight=0.70),
        HTARequirement("E1", "economic",
            "Cost data for price negotiation (not ICER-based)",
            mandatory=False, weight=0.60),
        HTARequirement("EP1", "epidemiological",
            "Patient population size in Germany",
            mandatory=True,  weight=0.80),
        HTARequirement("EP2", "epidemiological",
            "Current treatment landscape in Germany",
            mandatory=True,  weight=0.80),
        HTARequirement("R1", "rwe",
            "German claims or registry data",
            mandatory=False, weight=0.65),
        HTARequirement("R2", "rwe",
            "Literature search less than 3 months old at submission date",
            mandatory=True, weight=0.70),
    ]


def build_has_requirements() -> List[HTARequirement]:
    """
    HAS SMR/ASMR rating requirement matrix.

    HAS rates clinical benefit as SMR (Service Medical Rendu)
    and added benefit as ASMR (Amelioration du SMR) on a
    5-level scale from I (major improvement) to V (no improvement).

    ASMR rating directly drives the price negotiated with CEPS.
    Strong ASMR claim requires robust comparative clinical data.
    ICER model is optional but strengthens negotiating position.
    """
    return [
        HTARequirement("C1", "clinical",
            "Phase III RCT versus SMR-relevant comparator",
            mandatory=True,  weight=1.00),
        HTARequirement("C2", "clinical",
            "ASMR claim supported by clinical endpoint data",
            mandatory=True,  weight=0.95),
        HTARequirement("C3", "clinical",
            "Overall survival and progression-free survival data",
            mandatory=True,  weight=0.90),
        HTARequirement("C4", "clinical",
            "QoL data using French validated instruments",
            mandatory=True,  weight=0.80),
        HTARequirement("C5", "clinical",
            "Direct or adjusted indirect comparisons",
            mandatory=False, weight=0.75),
        HTARequirement("E1", "economic",
            "ICER model — optional but strengthens CEPS negotiation",
            mandatory=False, weight=0.70),
        HTARequirement("E2", "economic",
            "Budget impact from Assurance Maladie perspective",
            mandatory=False, weight=0.75),
        HTARequirement("EP1", "epidemiological",
            "French epidemiology — incidence and prevalence",
            mandatory=True,  weight=0.85),
        HTARequirement("R1", "rwe",
            "French registry or claims data",
            mandatory=False, weight=0.65),
        HTARequirement("R2", "rwe",
            "Real-world effectiveness data post-approval",
            mandatory=False, weight=0.60),
    ]


# Master dictionary of all HTA bodies
HTA_BODIES = {
    "NICE (UK)": build_nice_requirements(),
    "G-BA (DE)": build_gba_requirements(),
    "HAS (FR)":  build_has_requirements(),
}


if __name__ == "__main__":
    for body, reqs in HTA_BODIES.items():
        mandatory = sum(1 for r in reqs if r.mandatory)
        supportive = sum(1 for r in reqs if not r.mandatory)
        print(f"{body}: {len(reqs)} requirements "
              f"({mandatory} mandatory, {supportive} supportive)")