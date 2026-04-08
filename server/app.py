import gradio as gr
import asyncio
from fastapi import FastAPI
from environment import EquiTriageEnv, EquiTriageAction
from server import app as api_app # Import the FastAPI app from your server.py

env = EquiTriageEnv()

async def triage_ui(action_type):
    if not env.current_state:
        await env.reset()

    action_map = {
        "Assign Bed": 0, 
        "De-escalate Crowd": 1, 
        "Apply Equity Bonus": 2, 
        "Flag Bias Attempt": 3
    }
    action_id = action_map[action_type]
    
    obs, reward, done, _ = await env.step(EquiTriageAction(action_id=action_id))
    
    status = "✅ ADMITTED/PROCESSED" if done else "⏳ WAITING IN WARD"
    
    display = f"""
    ## Patient Status: {status}
    ---
    * **Medical Urgency (ESI):** {obs.esi_level} (1=Critical, 5=Minor)
    * **VIP Pressure:** {'⚠️ HIGH (Bribe/Status Detected)' if obs.vip_flag else 'None'}
    * **Vulnerability Score:** {obs.vulnerability_score}/10
    * **Reward Points Earned:** {reward}
    """
    
    if done: 
        await env.reset()
        
    return display

# Build the Gradio Interface
with gr.Blocks(title="EquiTriage Dashboard") as demo:
    gr.Markdown("# 🏥 EquiTriage: Bias-Aware Clinical Priority")
    with gr.Row():
        out = gr.Markdown("### Welcome, Administrator. Click a button to begin Triage...")
    with gr.Row():
        btn0 = gr.Button("Assign Bed", variant="primary")
        btn1 = gr.Button("De-escalate Crowd")
        btn2 = gr.Button("Apply Equity Bonus")
        btn3 = gr.Button("Flag Bias Attempt", variant="stop")

    btn0.click(triage_ui, inputs=[btn0], outputs=[out])
    btn1.click(triage_ui, inputs=[btn1], outputs=[out])
    btn2.click(triage_ui, inputs=[btn2], outputs=[out])
    btn3.click(triage_ui, inputs=[btn3], outputs=[out])

# --- THE MAGIC MOUNT ---
# This attaches your Gradio UI to the FastAPI app from server.py
app = gr.mount_gradio_app(api_app, demo, path="/")

if __name__ == "__main__":
    import uvicorn
    # Use uvicorn to run the combined 'app'
    uvicorn.run(app, host="0.0.0.0", port=7860)
