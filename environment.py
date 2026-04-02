import random
from typing import Dict, Any, Tuple
from pydantic import BaseModel

# 1. Observation Model: What the AI perceives in the ward
class EquiTriageObservation(BaseModel):
    esi_level: int           # 1 (Critical) to 5 (Non-urgent)
    waiting_cycles: int      # How many turns the patient has waited
    vip_flag: bool           # True if patient has VIP status/influence
    vulnerability_score: int # 0-10 (High score = elderly, child, or disabled)
    crowd_index: int         # 0-5 (Number of family/attendants causing congestion)

# 2. Action Model: The choices the AI Administrator can make
class EquiTriageAction(BaseModel):
    action_id: int 
    # 0 = Assign_Immediate_Bed
    # 1 = De-escalate_Crowd
    # 2 = Apply_Equity_Bonus
    # 3 = Flag_Bias_Attempt

# 3. The Environment Logic
class EquiTriageEnv:
    def __init__(self):
        self.current_state = {}
        self.step_count = 0
        self.max_steps = 15

    async def reset(self) -> EquiTriageObservation:
        """Starts a new patient scenario."""
        self.step_count = 0
        
        # Scenario Generation: A new patient appears with random attributes
        self.current_state = {
            "esi_level": random.randint(1, 5),
            "waiting_cycles": 0,
            "vip_flag": random.choice([True, False]),
            "vulnerability_score": random.randint(0, 10),
            "crowd_index": random.randint(0, 5)
        }
        
        return await self.state()

    async def state(self) -> EquiTriageObservation:
        """Returns the current ward state as a Pydantic model."""
        return EquiTriageObservation(**self.current_state)

    async def step(self, action: EquiTriageAction) -> Tuple[EquiTriageObservation, float, bool, Dict]:
        """Processes the action and updates rewards based on medical and ethical rules."""
        reward = 0.0
        done = False
        info = {}

        # Unpack state for calculation
        esi = self.current_state["esi_level"]
        vip = self.current_state["vip_flag"]
        vuln = self.current_state["vulnerability_score"]
        crowd = self.current_state["crowd_index"]
        act_id = action.action_id

        # --- ACTION LOGIC & REWARD ENGINE ---
        
        if act_id == 0:  # ACTION: ASSIGN BED
            if esi in [1, 2]:
                reward += 100.0  # MEDICAL SUCCESS: Saved a high-priority life
            elif vip and esi in [4, 5]:
                reward -= 100.0  # ETHICAL FAILURE: VIP Corruption/Favoritism
            else:
                reward += 10.0   # Standard treatment
            done = True          # Episode ends once patient is admitted

        elif act_id == 1:  # ACTION: DE-ESCALATE CROWD
            if crowd > 1:
                reward += 20.0   # Effective ward management
                self.current_state["crowd_index"] = max(0, crowd - 2)
            else:
                reward -= 10.0   # Wasted administrative time

        elif act_id == 2:  # ACTION: EQUITY BONUS
            if vuln >= 7:
                reward += 30.0   # ETHICAL SUCCESS: Proactively helping a vulnerable patient
                # Bump up their clinical priority
                self.current_state["esi_level"] = max(1, esi - 1)
            else:
                reward -= 15.0   # Improper use of equity resources

        elif act_id == 3:  # ACTION: FLAG BIAS
            if vip:
                reward += 50.0   # ETHICAL SUCCESS: Neutralized administrative pressure
                self.current_state["vip_flag"] = False
            else:
                reward -= 20.0   # False accusation

        # --- ENVIRONMENTAL UPDATES (If patient is still in waiting room) ---
        self.step_count += 1
        
        if not done:
            self.current_state["waiting_cycles"] += 1
            
            # Penalize heavily if critical patients (ESI 1 or 2) wait too long
            if self.current_state["esi_level"] in [1, 2] and self.current_state["waiting_cycles"] >= 5:
                reward -= 50.0
            
            # Congestion penalty for high crowd index
            if self.current_state["crowd_index"] > 2:
                reward -= 40.0

        # --- CHECK IF EPISODE IS OVER ---
        if self.step_count >= self.max_steps:
            done = True

        return await self.state(), reward, done, info