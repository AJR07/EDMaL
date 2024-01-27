from transformers import pipeline, set_seed

def regenerate(text: str): 
	generator = pipeline('text-generation', model='gpt2-large')
	set_seed(1)
	return generator(text, max_length=2*len(text), num_return_sequences=1)[0]['generated_text']