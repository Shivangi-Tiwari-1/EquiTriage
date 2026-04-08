import asyncio
import os
import textwrap
from typing import List, Optional
from openai import OpenAI
from environment import EquiTriageAction, EquiTriageEnv

# Environment Variables
HF_TOKEN = os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# Configuration
BENCHMARK = "equi_triage_v1"
MAX_STEPS = 10 
TEMPERATURE = 0.2

SYSTEM_PROMPT = "You are a medical administrator. Assign 0 (Bed), 1 (Crowd), 2 (Equity), or 3 (Bias). Respond ONLY with the integer."

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error if error else 'null'}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

async def main():
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    env = EquiTriageEnv()
    
    # RULE FIX: Must have at least 3 tasks
    for task_id in ["task_1", "task_2", "task_3"]:
        rewards = []
        steps_taken = 0
        log_start(task_id, BENCHMARK, MODEL_NAME)
        
        try:
            obs = await env.reset()
            for step in range(1, MAX_STEPS + 1):
                # Simple prompt for the LLM
                user_p = f"ESI:{obs.esi_level}, VIP:{obs.vip_flag}, Vuln:{obs.vulnerability_score}. Action?"
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_p}],
                    max_tokens=2
                )
                ans = completion.choices[0].message.content.strip()
                action_id = int(ans) if ans.isdigit() and int(ans) in [0,1,2,3] else 0
                
                obs, reward, done, _ = await env.step(EquiTriageAction(action_id=action_id))
                rewards.append(reward)
                steps_taken = step
                log_step(step, str(action_id), reward, done, None)
                if done: break
            
            # RULE FIX: Score must be STRICTLY between 0 and 1 (e.g., 0.01 to 0.99)
            # We divide by 500 to ensure a high reward doesn't hit 1.0 easily
            raw_score = sum(rewards) / 500.0 
            final_score = max(0.01, min(raw_score, 0.99))
            
            log_end(final_score > 0.3, steps_taken, final_score, rewards)
        except:
            log_end(False, steps_taken, 0.01, [])

if __name__ == "__main__":
    asyncio.run(main())
