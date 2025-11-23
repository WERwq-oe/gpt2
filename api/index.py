from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)
CORS(app)

# Add parent directory to path to import training modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model_artifacts")

model = None
tokenizer = None

def load_model():
    global model, tokenizer
    try:
        if os.path.exists(MODEL_DIR):
            print("Loading model from artifacts...")
            tokenizer = GPT2Tokenizer.from_pretrained(MODEL_DIR)
            model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            model.eval()
            print("Model loaded successfully.")
        else:
            print("Model artifacts not found. Using fallback.")
    except Exception as e:
        print(f"Error loading model: {e}")

load_model()

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    vibe = data.get('vibe', 'Professional')
    
    full_prompt = f"Prompt: {prompt} ({vibe})\nBio:"
    
    if model and tokenizer:
        try:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            input_ids = tokenizer.encode(full_prompt, return_tensors='pt').to(device)
            
            with torch.no_grad():
                output = model.generate(
                    input_ids, 
                    max_length=100, 
                    temperature=0.9, 
                    top_k=50,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
            bio = decoded_output.split("Bio:")[1].strip() if "Bio:" in decoded_output else decoded_output
            return jsonify({"bio": bio})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        # Fallback for demo/Vercel without large model
        return jsonify({
            "bio": f"✨ {vibe} Bio: {prompt} - Crafted with precision. A visionary approach to {prompt.split()[-1] if prompt else 'life'}. #FutureReady"
        })

if __name__ == '__main__':
    app.run(debug=True, port=5328)
