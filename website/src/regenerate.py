from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2-large')
set_seed(1)

def regenerate(text: str): 
	result = generator(f"Continue the following text: " + text, max_length=1024, num_return_sequences=1)
	return result[0]['generated_text']