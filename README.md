# HTA Dossier Gap Analysis Tool

**NICE, G-BA, and HAS Evidence Gap Mapper with Weighted Readiness Scoring**

---

## The Problem

Regulatory approval and HTA approval are two different things.

A drug can get FDA or EMA approval and still not be reimbursed
for 6 to 18 months because the HTA dossier has a critical gap.
NICE needs EQ-5D with UK tariff. G-BA needs head-to-head data
versus the appropriate comparator (gAV). HAS needs a strong
ASMR claim supported by comparative endpoints.

Getting this wrong costs months of reimbursement delay and
millions in lost revenue.

---

## What This Tool Does

- Maps a sponsor evidence inventory against NICE, G-BA, and HAS
  requirement matrices
- Flags every mandatory gap as CRITICAL
- Computes weighted readiness score per HTA body
- Assigns RAG status — Green, Amber, or Red
- Exports gap report per market and a cross-market summary

---

## Model Assumptions

| Parameter | Value | Notes |
|---|---|---|
| HTA bodies | 3 | NICE UK, G-BA Germany, HAS France |
| Evidence items | 16 | Phase III oncology asset at data cut |
| Mandatory score threshold GREEN | 80% | No critical gaps required |
| Mandatory score threshold AMBER | 60% | Up to 2 critical gaps allowed |
| Quality scale | 0.0 to 1.0 | Gold standard RCT = 0.95 |

---

## Key Output

HTA Body    Overall  Mandatory  Critical Gaps  RAG
NICE (UK)   72.1%    74.3%      2              AMBER
G-BA (DE)   71.4%    76.2%      2              AMBER
HAS (FR)    65.3%    78.6%      1              AMBER
Total critical gaps: 4
Most critical market: G-BA (DE)

---

## The Scoring Formula

weighted_score = status_score x quality x requirement_weight
status scores:
available   = 1.00
partial     = 0.50
planned     = 0.25
unavailable = 0.00
RAG logic:
GREEN = 0 critical gaps AND mandatory score >= 80%
AMBER = <= 2 critical gaps AND mandatory score >= 60%
RED   = > 2 critical gaps OR mandatory score < 60%

---

## Quick Start

```bash
git clone https://github.com/sannapa2016/hta-dossier-gap-tool.git
cd hta-dossier-gap-tool
pip install -r requirements.txt
pip install -e .
python main.py
```

---

## Project Structure

hta-dossier-gap-tool/
├── src/
│   ├── init.py              Makes src a Python package
│   ├── hta_requirements.py      NICE, G-BA, HAS requirement matrices
│   ├── evidence.py              Sponsor evidence inventory
│   └── gap_analyzer.py          Scoring engine and RAG logic
├── outputs/                     CSV results generated on run
├── main.py                      Single entry point
└── requirements.txt             pandas, numpy

---

## Connection to Project 1 — IRP Cascade Simulator

HTA timelines constrain the IRP launch sequence directly.

- Germany G-BA: 3 months from approval to decision
- France HAS: 6 to 9 months
- UK NICE: 12 to 18 months

A market cannot be reimbursed until HTA approval is obtained.
This tool tells you whether your evidence is ready for each
HTA body so launch sequencing decisions are grounded in
evidence readiness not just pricing strategy.

---

## Author

**Siva Annapareddy**
Founder and AVP, Amrak Pharma Analytics
18 years in pharma commercial analytics

*Project 4 of 36 — open-source pharma analytics portfolio*

