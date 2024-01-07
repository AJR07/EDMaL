# Script: Generate Reddit Small Dataset (Human + AI)

import os
from cleantext import clean
import tqdm
import re
import nltk
from nltk.tokenize import word_tokenize
import openai
import random

# Utility function to save an array to a file
def save(uttr_current, file_name):
    with open(file_name, "w") as f:
        for utt in uttr_current:
            f.write(str(utt) + "\n------\n")

generate_human = input("Human dataset generated? (0 for no)")
human_utterances = []
if generate_human == 0:
    from convokit import Corpus, download
    #! generate human dataset
    corpus = Corpus(filename=download("reddit-corpus-small"))
    corpus.print_summary_stats()

    # save the raw utterances into a txt file	
    utterances = []
    for utt in corpus.iter_utterances():
        utterances.append(utt.text)
    save(utterances, "raw-human.txt")
    print("Raw Data Saved")

    # prune the raw dataset

    # use of clean-text to strip various un-needed information
    # https://pypi.org/project/clean-text/

    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)

    for utt_idx in tqdm.tqdm(range(len(utterances))):
        utterances[utt_idx] = clean(utterances[utt_idx],
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
        utterances[utt_idx] = emoji_pattern.sub(r'', utterances[utt_idx]) # no emoji
    print(f"Size of dataset after step 1: {len(utterances)}")
    
    # Remove utterances < 20 characters and > 300 characters
    utterances = [utt for utt in utterances if len(utt) >= 20 and len(utt) <= 300]
    print(f"Size of dataset after step 2: {len(utterances)}")

    # Remove repeated utterances
    utterances = list(set(utterances))
    print(f"Size of dataset after step 3: {len(utterances)}")

    # Save pruned dataset
    save(utterances, "pruned-human.txt")
    print("Pruned Data Saved")

    # Tokenize Data
    nltk.download('punkt')
    tokenized_human = []
    utterances_human = utterances

    for utt_idx in tqdm.tqdm(range(len(utterances))):
        tokenized_human.append(' '.join(word_tokenize(utterances[utt_idx])))

    # Save tokenized data
    save(tokenized_human, "tokenized.txt")
    print("Tokenized Data Saved")

else:
    utterances_human = []
    with open("../reddit_min100/pruned_human.txt", "r") as f:
        lines = f.readlines()
        lines = '\n'.join(lines)
        utterances_human = lines.split('\n------\n')
    print(f"Found: {len(utterances_human)} utterances")

print("Human Dataset Generation Done!")

#! generate AI dataset

# Using GPT-2 from huggingface, we generate separate
# sub-datasets representing: Create + Reply
# In a 50% - 50% ratio

# setup openAI
print("Generating AI Dataset...")
openai.api_key= "API_KEY"
os.environ['AZURE_OPENAI_ENDPOINT']= "API_ENDPOINT"
openai.api_type = "API_TYPE"
openai.api_version = "API_DATE"

# generate REPLIES
print("Generating Replies...")
utterances_ai_reply = []
for utterance_human_idx in tqdm.tqdm(range(1250)):
  # try-except as a cheeky way to continue generation if API call does not work
  while True:
    try:
      # 0-shot reply generation
      txt = f"""As a helpful reply-to-reddit-posts assistant, please reply to this post informally and impolitely, keeping your response as human-like as posisble and at a minimum of 100 words (No need to state your identitiy at the start):
{utterances_human[int(random.random() * len(utterances_human))]}
"""
      # generate
      res = openai.chat.completions.create(
          model= "MODEL_NAME",
          messages=[
              {
                  "role": "user",
                  "content": txt
              }
          ],
          temperature=0.6,
          max_tokens=4000,
          presence_penalty=-0.5
      )
      res = res.choices[0].message.content

      # prevent too many posts created that are actually just the AI aplogising
      if res == None or "I'm sorry, but I" in res:
        raise Exception("I'm sorry")

      utterances_ai_reply.append(res)
      break
    except Exception as e:
      print(f"Exception: {e}")
      
print("Saving AI Dataset...")
save(utterances_ai_reply, "reply_ai.txt")

# generate CREATES
print("Generating Creates...")

utterances_ai_create = []
for utterance_human_idx in tqdm.tqdm(range(1250)):
  # try-except as a cheeky way to continue generation if API call does not work
  while True:
    # 1-shot creation of a new Reddit Post based on other Reddit Posts
    txt = f"Imagine if you are a casual Reddit User, scrolling through a subreddit. Please create an informal and impolite post on a new thread in this subreddit, while keeping your response at a minimum of 100 words. Here's a sample post for your reference (No need for title):\n{utterances_human[int(random.random() * len(utterances_human))]}"

    try:
      # generate
      res = openai.chat.completions.create(
          model= "MODEL_NAME",
          messages=[
              {
                  "role": "user",
                  "content": txt
              }
          ],
          temperature=0.9,
          max_tokens=4000,
          presence_penalty=0.5
      )
      res = res.choices[0].message.content

      # prevent too many posts created that are actually just the AI aplogising
      if res == None or "I'm sorry, but I" in res:
        raise Exception("I'm sorry")

      utterances_ai_create.append(res)
      break
    except Exception as e:
      print(f"Exception: {e}")

print("Saving AI Dataset...")
save(utterances_ai_create, "create_ai.txt")

print("Generation Done!")