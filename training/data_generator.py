import csv
import random
import os

# Configuration
OUTPUT_FILE = "training/bio_dataset.csv"
NUM_SAMPLES = 500  # Number of synthetic samples to generate

# Vocabulary and Templates
adjectives = [
    "Visionary", "Passionate", "Dedicated", "Creative", "Innovative", "Driven",
    "Eclectic", "Stoic", "Vibrant", "Authentic", "Maverick", "Quixotic",
    "Sanguine", "Resilient", "Empathetic", "Dynamic", "Versatile", "Intrepid"
]

nouns = [
    "Creator", "Innovator", "Artist", "Developer", "Strategist", "Dreamer",
    "Explorer", "Architect", "Catalyst", "Philosopher", "Nomad", "Alchemist",
    "Storyteller", "Evangelist", "Maven", "Virtuoso"
]

interests = [
    "Tech", "AI", "Art", "Design", "Fitness", "Travel", "Music", "Writing",
    "Photography", "Startup", "Blockchain", "Sustainability", "Coffee", "Code"
]

verbs = [
    "Building", "Crafting", "Designing", "Exploring", "Reimagining", "Disrupting",
    "Coding", "Writing", "Curating", "Orchestrating", "Navigating", "Synthesizing"
]

templates = [
    "{adj} {noun} | {verb} the future of {interest}.",
    "{verb} {interest} with a {adj} perspective.",
    "{noun} at heart. {adj} in spirit. {verb} {interest}.",
    "Just a {adj} {noun} obsessed with {interest} and {interest}.",
    "Turning {interest} into reality. {adj} {noun}.",
    "{adj} soul. {noun} mind. {verb} {interest} daily.",
    "Redefining {interest} through the lens of a {adj} {noun}."
]

def generate_bio():
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    verb = random.choice(verbs)
    int1 = random.choice(interests)
    int2 = random.choice(interests)
    while int1 == int2:
        int2 = random.choice(interests)
    
    template = random.choice(templates)
    bio = template.format(adj=adj, noun=noun, verb=verb, interest=int1)
    
    # Add some variation
    if random.random() > 0.7:
        bio += f" 📍 {random.choice(['NYC', 'SF', 'London', 'Tokyo', 'Remote'])}"
    
    return bio

def generate_dataset():
    print(f"Generating {NUM_SAMPLES} samples...")
    data = []
    for _ in range(NUM_SAMPLES):
        prompt = "Generate a bio" # In a real scenario, this could be more specific
        bio = generate_bio()
        data.append([prompt, bio])
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["prompt", "completion"]) # GPT-2 fine-tuning format often uses simple text, but CSV is good for custom loaders
        writer.writerows(data)
    
    print(f"Dataset saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs("training", exist_ok=True)
    generate_dataset()
