import asyncio
from environment import EquiTriageEnv, EquiTriageAction

async def test():
    env = EquiTriageEnv()
    print("\n--- STARTING HOSPITAL SIMULATION ---")
    obs = await env.reset()
    print(f"New Patient Arrived: {obs}")

    # Simulate an action (Action 0 = Assign Bed)
    print("\nAction: Assigning Bed...")
    obs, reward, done, _ = await env.step(EquiTriageAction(action_id=0))
    
    print(f"Result: Reward = {reward}, Episode Done = {done}")
    print(f"Current Ward State: {obs}")

if __name__ == "__main__":
    asyncio.run(test())