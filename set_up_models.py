
from transformers import pipeline
from pytorch_transformers import GPT2Tokenizer, GPT2LMHeadModel
import os


# Translation pipeline with M2M100, an LLM from Facebook AI that can translate between 100 languages
_my_pipe = None
def translate(text):
    global _my_pipe
    if _my_pipe is None:
        _my_pipe = pipeline(task="text2text-generation", model="facebook/m2m100_418M", device=-1) # *** currently cpu
    temp = _my_pipe(text, forced_bos_token_id=_my_pipe.tokenizer.get_lang_id(lang="es")) # "es" to indicate translation into Spanish
    return temp[0]["generated_text"]


# GPT-2 model & tokenizer: save them only if they are not already saved at that path
_model = None
_tokenizer = None
def get_gpt2():
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        model_path = "models/gpt2"
        tokenizer_path = "models/gpt2_tokenizer"
        os.makedirs(model_path, exist_ok=True)
        os.makedirs(tokenizer_path, exist_ok=True)
        if not os.listdir(model_path):
            model = GPT2LMHeadModel.from_pretrained("gpt2")
            model.save_pretrained(model_path)
        if not os.listdir(tokenizer_path):
            tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
            tokenizer.save_pretrained(tokenizer_path)
        _model = GPT2LMHeadModel.from_pretrained(model_path)
        _tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return _model, _tokenizer