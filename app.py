import gradio as gr
import asyncio
from environment import EquiTriageEnv, EquiTriageAction

env = EquiTriageEnv()

async def triage_ui(action_type):
    # Map button names to Action IDs from your environment
    action_map = {"Assign Bed": 0, "De-escalate": 1, "Equity Bonus": 2, "Flag Bias": 3}
    action_id = action_map[action_type]
    
    # Run the logic
    obs, reward, done, _ = await env.step(EquiTriageAction(action_id=action_id))
    
    status = "✅ ADMITTED/PROCESSED" if done else "⏳ WAITING IN WARD"
    
    # Create the visual status card
    display = f"""
    ## Patient Status: {status}
    ---
    * **Medical Urgency (ESI):** {obs.esi_level} (1=Critical, 5=Minor)
    * **VIP Pressure:** {'⚠️ HIGH (Bribe/Status Detected)' if obs.vip_flag else 'None'}
    * **Vulnerability Score:** {obs.vulnerability_score}/10
    * **Reward Points Earned:** {reward}
    """
    
    if done: 
        await env.reset() # Automatically bring in a new patient if the last one was admitted
        
    return display

# Build the Interface
with gr.Blocks(title="EquiTriage Dashboard") as demo:
    gr.Markdown("# 🏥 EquiTriage: Bias-Aware Clinical Priority")
    gr.Markdown("An AI-driven environment for ethical medical triage and anti-corruption logic.")
    
    with gr.Row():
        out = gr.Markdown("### Welcome, Administrator. Click a button to begin Triage...")
        
    with gr.Row():
        btn0 = gr.Button("Assign Bed", variant="primary")
        btn1 = gr.Button("De-escalate Crowd")
        btn2 = gr.Button("Apply Equity Bonus")
        btn3 = gr.Button("Flag Bias Attempt", variant="stop")

    # Connect buttons to the logic
    btn0.click(triage_ui, inputs=[btn0], outputs=[out])
    btn1.click(triage_ui, inputs=[btn1], outputs=[out])
    btn2.click(triage_ui, inputs=[btn2], outputs=[out])
    btn3.click(triage_ui, inputs=[btn3], outputs=[out])

if __name__ == "__main__":
    # Crucial: This port (7860) and server_name are required for Hugging Face Spaces
    demo.launch(server_name="0.0.0.0", server_port=7860)