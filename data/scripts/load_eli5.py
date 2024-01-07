import datasets
import argparse
import os
import openai
import tqdm
import re
from cleantext import clean

#! Script Parameters
parser = argparse.ArgumentParser()

# openai identification
parser.add_argument('--api_key', default='API_KEY')
parser.add_argument('--api_endpoint', default="API_ENDPOINT")
parser.add_argument('--api_type', default='API_TYPE')
parser.add_argument('--api_version', default='2023-05-15')

args = parser.parse_args()

#! Prepare OpenAI parameters
openai.api_key = args.api_key
os.environ['AZURE_OPENAI_ENDPOINT'] = args.api_endpoint
openai.api_type = args.api_type
openai.api_version = args.api_version

db = datasets.load_dataset("eli5")

def save(uttr_current, file_name):
  with open(file_name, "w") as f:
    for utt in uttr_current:
        f.write(str(utt) + "\n------\n")

#! Generate Human Dataset
db = list(db["train_askh"]) + list(db["train_asks"]) + list(db["train_eli5"])
db = db[:100000]
print("Dataset Loaded!")
human_utterances = []
ai_questions = []

for idx in tqdm.tqdm(range(len(db))):
	instance = db[idx]
	human_utterances.append(instance["answers"]["text"][0])
	ai_questions.append(instance["title"])

emoji_pattern = re.compile("["
		u"\U0001F600-\U0001F64F"  # emoticons
		u"\U0001F300-\U0001F5FF"  # symbols & pictographs
		u"\U0001F680-\U0001F6FF"  # transport & map symbols
		u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
						"]+", flags=re.UNICODE)

for utt_idx in tqdm.tqdm(range(len(human_utterances))):
	human_utterances[utt_idx] = clean(human_utterances[utt_idx],
		fix_unicode=True,
		to_ascii=True,
		lower=True,
		no_urls=True,
		no_emails=True,
		no_phone_numbers=True,
		no_currency_symbols=True,
		replace_with_url="<URL>",
		replace_with_email="<EMAIL>",
		replace_with_phone_number="<PHONE>",
		replace_with_currency_symbol="<CUR>",
		lang="en"
		)
	human_utterances[utt_idx] = emoji_pattern.sub(r'', human_utterances[utt_idx]) # no emoji
print(f"Size of dataset after step 1: {len(human_utterances)}")

# Remove utterances > 100 characters
human_utterances = [utt for utt in human_utterances if len(utt) >= 500]
print(f"Size of dataset after step 2: {len(human_utterances)}")

# Remove repeated utterances
human_utterances = list(set(human_utterances))
print(f"Size of dataset after step 3: {len(human_utterances)}")

save(human_utterances, "pruned_human_eli5.txt")
save(ai_questions, "ai_questions_eli5.txt")

#! Generate AI Dataset
print("Generating AI Dataset...")

ai_utterances = []
for idx in tqdm.tqdm(range(0, 2500)):
	try:
		res = openai.chat.completions.create(
			model= "MODEL_NAME",
			messages=[
				{
					"role": "system",
					"content": "You are a Reddit User informally and casually answering Answer-Me-Like-I-Am-5 questions on Reddit. Please provide a minimum of a 100 word detailed and well-elaborated essay answering the question provided."
				},
				{
					"role": "user",
					"content": ai_questions[idx]
				}
			],
			temperature=0.7,
			max_tokens=4000,
			presence_penalty=0.5
		)
		res = res.choices[0].message.content
		ai_utterances.append(res)
	except Exception as e:
		print(e)


save(ai_utterances, "raw_ai_eli5.txt")
print("Generation Done!")