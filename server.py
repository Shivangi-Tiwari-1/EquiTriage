from fastapi import FastAPI
from environment import EquiTriageEnv, EquiTriageAction

app = FastAPI()
env = EquiTriageEnv()

@app.post("/reset")
async def reset():
    obs = await env.reset()
    return {"observation": obs.dict()}

@app.post("/step")
async def step(action: EquiTriageAction):
    obs, reward, done, info = await env.step(action)
    return {"observation": obs.dict(), "reward": reward, "done": done, "info": info}

@app.get("/state")
async def state():
    obs = await env.state()
    return {"observation": obs.dict()}