# Python program to finetune Generative Pre-trained Transformer 2 (GPT-2) with a text file.

from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import Trainer, TrainingArguments

ruler_file = r"--path of file to finetune gpt2---"
model_name = r'gpt2'
output_dir = r'--directory of the output model--'
per_device_train_batch_size = 8
num_train_epochs = 5.0

# tokens for the model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# create fine tuning datasets using tokeniser and fine tune file
train_data = TextDataset(tokenizer = tokenizer,file_path = ruler_file, block_size=256)
# preprocess the data
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
# get the gpt2 model
model = GPT2LMHeadModel.from_pretrained(model_name)

# ready the above for training 
trainer = Trainer(
        args = TrainingArguments(output_dir=output_dir,\
               per_device_train_batch_size=per_device_train_batch_size,\
               num_train_epochs=num_train_epochs),
        model=model,
        data_collator=data_collator,
        train_dataset=train_data,
)

# start finetuning
trainer.train()
# save the finetuned model 
trainer.save_model()

# use the finetuned model to generate text using input tokens
tokenizer = GPT2Tokenizer.from_pretrained(output_dir)
model = GPT2LMHeadModel.from_pretrained(output_dir, pad_token_id=tokenizer.eos_token_id)
text = tokenizer.encode("--some text --", return_tensors='pt')

# limit the output to 1000 words in case early stopping doesn't happen, and limit repeatition of text to atmost 2 lines and random sample from the response generated
output = model.generate(text,
                        max_length = 1000,  
                        no_repeat_ngram_size = 2, 
                        early_stopping = True,
                        num_beams = 2,
                        do_sample=True)

# print the output
print(tokenizer.decode(output[0], skip_special_tokens=True))

