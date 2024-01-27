from cleantext import clean
import re

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

def prune(txt: str):
	txt = clean(txt,
		fix_unicode=True,
		to_ascii=True,
		lower=True,
		no_urls=True,
		no_emails=True,
		no_phone_numbers=True,
		no_currency_symbols=True,
		lang="en"
	)
	txt = emoji_pattern.sub(r'', txt) # no emoji

	return txt