import os
import csv
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from torch.optim import AdamW

# Configuration
DATA_FILE = "training/bio_dataset.csv"
OUTPUT_DIR = "model_artifacts"
EPOCHS = 3
BATCH_SIZE = 4
LEARNING_RATE = 5e-5
MAX_LEN = 128
MODEL_NAME = "gpt2" # Using base gpt2 for speed, can use gpt2-medium/large for better quality

class BioDataset(Dataset):
    def __init__(self, filename, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.data = []
        self.max_length = max_length
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            for row in reader:
                if len(row) >= 2:
                    # Format: Prompt: <prompt> \n Bio: <bio> <eos>
                    text = f"Prompt: {row[0]}\nBio: {row[1]}{tokenizer.eos_token}"
                    self.data.append(text)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]
        encodings = self.tokenizer(text, truncation=True, max_length=self.max_length, padding="max_length", return_tensors="pt")
        input_ids = encodings['input_ids'].squeeze()
        attention_mask = encodings['attention_mask'].squeeze()
        return input_ids, attention_mask

def train():
    print(f"Loading {MODEL_NAME} model and tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained(MODEL_NAME)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    model.train()
    
    dataset = BioDataset(DATA_FILE, tokenizer, MAX_LEN)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    
    print("Starting training...")
    for epoch in range(EPOCHS):
        total_loss = 0
        for step, (input_ids, attention_mask) in enumerate(loader):
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            
            outputs = model(input_ids, labels=input_ids, attention_mask=attention_mask)
            loss = outputs.loss
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if step % 10 == 0:
                print(f"Epoch {epoch+1}/{EPOCHS} | Step {step}/{len(loader)} | Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch+1} complete. Average Loss: {avg_loss:.4f}")

    print("Saving model...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print(f"Model saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    train()
