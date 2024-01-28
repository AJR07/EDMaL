from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2-large')
set_seed(1)

def regenerate(text: str): 
	result = generator("Imagine you are an accurate complete-the-text assistant. You stumble across the first half of text written by a Large Language Model like yourself. You do not know the prompt provided to the Large Language Model, but you are tasked with generating the latter half of the text, which is {len(masked_original)} characters long. Here is the text:" + text, max_length=1024, num_return_sequences=1)
	return result[0]['generated_text']