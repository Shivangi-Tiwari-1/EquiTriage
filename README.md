#  EquiTriage: A Bias-Aware Clinical Priority & Behavioral Dynamics Environment

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![OpenEnv](https://img.shields.io/badge/Framework-OpenEnv-orange) ![Status](https://img.shields.io/badge/Status-National_Hackathon_Submission-success)

> **"Solving the Priority Paradox in modern healthcare by balancing clinical urgency, social equity, and environmental order."**

##  Project Overview
**EquiTriage** is a high-fidelity Reinforcement Learning environment built atop the **OpenEnv** framework. While standard triage focuses purely on medical data, EquiTriage introduces **Social Logic** and **Behavioral Constraints**, forcing the AI to act as a "Fair Administrator" in high-pressure clinical settings.

---

##  Reward Architecture & Ethics Engine
EquiTriage is designed as a **Constraint-Satisfaction Environment**. The high-density penalties (-15 to -100) define the 'Social and Ethical Boundaries' of a hospital, while the sparse, high-value rewards (+100) ensure the agent remains laser-focused on the primary clinical mission: saving lives.

### Reward Function Distribution
| Component | Metric | Weight | Ethical/Operational Goal |
|:---|:---|:---|:---|
| **Clinical** | ESI 1/2 Treatment | **+100** | Life-Saving Priority |
| **Equity** | Vulnerability Bonus | **+30** | Support for Children/Elderly |
| **Integrity** | VIP Corruption Penalty | **-100** | Zero-Tolerance for Status Bias |
| **Temporal** | Waiting Deterioration | **-50 (2x)** | Real-time Risk Mitigation |
| **Behavioral** | Unauthorized Roaming | **-20** | Maintain Ward Order |
| **Acoustic** | Noise/Media Violation | **-15** | Patient Recovery Environment |
| **Spatial** | Seating Equity Violation | **-40** | Protect Vulnerable Comfort |
| **Logistics** | Crowd (Plus-One) Violation | **-40** | Prevent ER Congestion |

---

##  System Architecture

### 1. Clinical Decision Logic
The environment processes a "True Neutral" medical standard where physiological distress (ESI) overrides socio-economic status.

**Logic Flow:** `[Patient Input]` → `[ESI Acuity Check]` → `[Equity/Vulnerability Bias Check]` → `[Action Selection]`

### 2. Behavioral RL Loop
The agent interacts with the environment via the standard OpenEnv 3-method interface: `reset()`, `step()`, and `state()`.

**Feedback Loop:** `[State Observation]` → `[Agent Action]` → `[Multi-Objective Reward Calculation]` → `[Next State]`

---

##  Environment Rules (Logic Summary)
* **Clinical Objectivity:** A critical VIP is prioritized over a stable non-VIP (Medical need > Status).
* **The Suffocation Exception:** Roaming is penalized (-20) unless the state indicates "Medical Distress," allowing for survival instincts.
* **Crowd Control:** Attendants are limited to **1 per critical patient** and **0 for minor cases** to prevent ward congestion.
* **Temporal Decay:** Penalties for waiting double after 10 cycles for emergency cases to simulate patient deterioration.

---

##  The Team

**Team Leader:**
* SHIVANGI TIWARI 

**Team Members:**
* SHATAKSHI SINGH
* SHAGUN OMAR
