
import os

from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline


def translate(text):
    """Translate English text to Spanish using a pre-trained model."""
    _my_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
    result = _my_pipe(text)
    return result[0]["translation_text"]


def get_gpt2():
    """Load or download GPT-2 model and tokenizer, returning both."""
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