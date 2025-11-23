import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

MODEL_DIR = "model_artifacts"

def load_model():
    print("Loading model...")
    try:
        tokenizer = GPT2Tokenizer.from_pretrained(MODEL_DIR)
        model = GPT2LMHeadModel.from_pretrained(MODEL_DIR)
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def generate_bio_from_prompt(prompt, max_length=100, temperature=0.9, top_k=50):
    tokenizer, model = load_model()
    if not model:
        return "Model not found. Please train the model first."
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    input_text = f"Prompt: {prompt}\nBio:"
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)
    
    with torch.no_grad():
        output = model.generate(
            input_ids, 
            max_length=max_length, 
            temperature=temperature, 
            top_k=top_k,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Extract just the bio part
    try:
        bio = decoded_output.split("Bio:")[1].strip()
    except IndexError:
        bio = decoded_output
        
    return bio

if __name__ == "__main__":
    prompt = input("Enter a prompt (e.g., 'A creative designer'): ")
    print(generate_bio_from_prompt(prompt))
