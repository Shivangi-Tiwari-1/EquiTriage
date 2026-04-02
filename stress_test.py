import asyncio
from environment import EquiTriageEnv, EquiTriageAction

async def run_stress_test(total_patients=50):
    env = EquiTriageEnv()
    total_reward = 0
    vip_ignored = 0
    vulnerable_helped = 0
    lives_saved = 0

    print(f"--- SIMULATING {total_patients} PATIENTS ---")

    for _ in range(total_patients):
        obs = await env.reset()
        # Logic: If VIP, try to flag bias. If critical, assign bed.
        if obs.vip_flag:
            obs, reward, done, _ = await env.step(EquiTriageAction(action_id=3)) # Flag Bias
            vip_ignored += 1
        
        if obs.esi_level <= 2:
            obs, reward, done, _ = await env.step(EquiTriageAction(action_id=0)) # Assign Bed
            lives_saved += 1
            total_reward += reward

    print("\n--- FINAL REPORT ---")
    print(f"Total Patients Processed: {total_patients}")
    print(f"Critical Lives Saved: {lives_saved}")
    print(f"VIP Bias Attempts Neutralized: {vip_ignored}")
    print(f"Average Reward: {total_reward / total_patients:.2f}")

if __name__ == "__main__":
    asyncio.run(run_stress_test())