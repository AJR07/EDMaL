# This script takes a dataset of human and AI-generated utterances,
# splits the utterances into half-half, then masks the latter half.
# We then use a LLM to regenerate the latter half, so the AI-generated
# and the original latter half can be compared and evaluated
import argparse
import os
import openai
from tqdm import tqdm
import json
import time

#! Script Parameters
parser = argparse.ArgumentParser()

# dataset
parser.add_argument('--human_dataset', default="../data/pruned_human.txt", type=str) # non-tokenized, file-location
parser.add_argument('--ai_dataset', default="../data/raw_ai.txt", type=str) # non-tokenized, file-location
parser.add_argument('--results', default="./results.json", type=str)
parser.add_argument('--truncate_ratio', default=0.5, type=float)

# openai identification
parser.add_argument('--cert_location', default='/home/ajunray/certbundle.crt') # SSL_cert, set to Empty if not necessary
parser.add_argument('--api_key', default='API_KEY')
parser.add_argument('--api_endpoint', default="API_ENDPOINT")
parser.add_argument('--api_type', default='API_TYPE')
parser.add_argument('--api_version', default='API_DATE')

# openai models
parser.add_argument('--max_new_tokens', default=2048, type=int)
parser.add_argument('--regen_number', default=10, type=int)
parser.add_argument('--temperature', default= 0.5, type=float)
args = parser.parse_args()

#! Prepare OpenAI parameters
openai.api_key = args.api_key
os.environ['AZURE_OPENAI_ENDPOINT'] = args.api_endpoint
openai.api_type = args.api_type
openai.api_version = args.api_version

#! Load The Data
human_dataset = []
ai_dataset = []

# Read AI Dataset
with open(args.ai_dataset, "r") as f:
	lines = '\n'.join(f.readlines())
	ai_dataset = lines.split('\n------\n')

# Read Human Dataset
with open(args.human_dataset, "r") as f:
	lines = '\n'.join(f.readlines())
	human_dataset = lines.split('\n------\n')

# Combine Datasets
print(f"Done Reading Human Dataset, length: {len(human_dataset)}")
print(f"Done Reading AI Dataset, length: {len(ai_dataset)}")

if len(human_dataset) > len(ai_dataset):
	human_dataset = human_dataset[:len(ai_dataset)]
	print(f"Human Dataset shrunk to AI Dataset's Length of: {len(ai_dataset)}")

if len(human_dataset) < len(ai_dataset):
	ai_dataset = ai_dataset[:len(human_dataset)]
	print(f"AI Dataset shrunk to Human Dataset's Length of: {len(human_dataset)}")

combined_dataset = [{"type": "ai", "text": x} for x in ai_dataset] + [{"type": "human", "text": x} for x in human_dataset]
print(f"Combined Dataset's Length: {len(combined_dataset)}")

#! Truncate, Mask and Generate
final_dataset = []
for idx in tqdm(range(1, 5000, 4)):
	# truncate
	current_data = combined_dataset[idx]
	split_idx = int(len(current_data["text"])*args.truncate_ratio)
	unmasked_original = current_data["text"][:split_idx]
	masked_original = current_data["text"][split_idx:]

	# generate prompt to pass to openai's LLMs
	# while, try-catch to assist with error handling
	tries = 0
	while True:
		tries += 1
		if tries == 6:
			final_dataset.append({
				"type": combined_dataset[idx]["type"],
				"text": current_data["text"],
				"unmasked_original": unmasked_original,
				"masked_original": masked_original,
				"masked_generated": None
			})
			break
		try:
			res = openai.chat.completions.create(
				model= "MODEL_NAME",
                messages=[
					{"role": "system", "content": f"Imagine you are an accurate complete-the-text assistant. You stumble across the first half of text written by a Large Language Model like yourself. You do not know the prompt provided to the Large Language Model, but you are tasked with generating the latter half of the text, which is {len(masked_original)} characters long."},
                    {"role": "assistant", "content": unmasked_original},
                        
				], 
				temperature=args.temperature,
				max_tokens=args.max_new_tokens,
				n=args.regen_number
			)

			# after generating, append the data to the final dataset
			final_dataset.append({
				"type": combined_dataset[idx]["type"],
				"text": current_data["text"],
				"unmasked_original": unmasked_original,
				"masked_original": masked_original,
				"masked_generated": [(x.message.content if x.message.content != None else "") for x in res.choices]
			})
			break
		except Exception as e:
			print(f"An Exception has occured: {e}")

print("Done with generating!")

#! Save the data into a json file
print("Saving data into results.json...")
with open(args.results, "w+") as f:
	json.dump(final_dataset, f)
print("Done!")