# Use a pipeline as a high-level helper
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig

# tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")
# model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-Instruct-hf")


# Create a pipeline
# code_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
code_generator = pipeline("text-generation",
                          model=r"C:\Users\Misha\Desktop\CodeLlama-7b-hf",
                          truncation=True
                          )  # if you don't have GPU, remove this argument

# Generate code for an input string
input_string = "Write a python function to calculate the factorial of a number"
generated_code = code_generator(input_string, max_length=100)[0]['generated_text']
print(generated_code)
