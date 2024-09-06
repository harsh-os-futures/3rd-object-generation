import gradio as gr
import subprocess
import os
import re

def generate_save_path(prompt):
    # Generate a valid filename from the prompt by removing special characters
    sanitized_prompt = re.sub(r'[^\w\s]', '', prompt)  # Remove special characters
    words = sanitized_prompt.split()  # Split into words
    truncated_prompt = '_'.join(words[:4])  # Keep only the first 4 words and join them with underscores
    save_path = f"{truncated_prompt}"  # No file extension
    return save_path

def run_script(config_file, prompt):
    # Automatically generate save_path from prompt
    save_path = generate_save_path(prompt)
    
    # Command to run the script
    command = f"python main.py --config {config_file} prompt=\"{prompt}\" save_path={save_path}"
    
    # Run the command
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Provide the path to the output file for download
        if os.path.exists(save_path):
            return save_path
        else:
            return "File not found or script failed."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

# Gradio interface
iface = gr.Interface(
    fn=run_script,
    inputs=[
        gr.Textbox(label="Config File", value="configs/text.yaml"),
        gr.Textbox(label="Prompt", value="Carved pumpkin with scary face.")
    ],
    outputs=gr.File(label="Download File"),
    title="Run Main Script",
    description="Run main.py with specified parameters and download the output."
)

iface.launch()
