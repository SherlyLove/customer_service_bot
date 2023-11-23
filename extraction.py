import json
from datasets import load_dataset

# load the dataset
dataset = load_dataset("csv", data_files="Documents/Bitext_sample_customer_support_training_dataset.csv")
print(dataset)


# Initialize an empty intents list
intents = []

# Loop through the dataset
for data in dataset['train']:
    instruction = data['instruction']
    response = data['response']
    intent = data['category']

        
    # Check if intent exists
    intent_exists = False
    for existing_intent in intents:
        if existing_intent['tag'] == intent:
            intent_exists = True
            break
    
    # If intent does not exist, create a new one
    if not intent_exists:
        new_intent = {
            "tag": intent,
            "patterns": [],
            "responses": []
        }
        intents.append(new_intent)
        print(f"Intent: {intent}")
        
    # add question to patterns list of corresponding intent
    for existing_intent in intents:
        if existing_intent['tag'] == intent:
            existing_intent['patterns'].append(instruction)
        
    # add response to responses list of corresponding intent
    for existing_intent in intents:
        if existing_intent['tag'] == intent:
            existing_intent['responses'].append(response)
            break
            
# save intents to json file
with open("intents/intents-bitext-01.json", "w") as f:
    json.dump(intents, f, indent=4)
    
print("Extraction complete")