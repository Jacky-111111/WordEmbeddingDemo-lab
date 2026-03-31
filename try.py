from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
sample_text = "This is a sample sentence to test tokenization.  grandfather grandparent saxophone bassoon broccoli oboe intellectual"
tokens = tokenizer.encode(sample_text)

decoded = list(zip(tokens, [tokenizer.decode([tok]) for tok in tokens]))

for (tok,text) in decoded:
    print(f'{tok:5d} {text}')