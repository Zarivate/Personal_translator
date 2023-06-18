# File that handles DeepL API calls
import deepl
from dotenv import load_dotenv
import os

# Load the data held within the local .env file
load_dotenv()

# Set the DeepL Auth key
auth_key = os.getenv("DEEPL_AUTH_APIKEY")
# Set the translator
translator = deepl.Translator(auth_key)


# Function to make a call to DeepL API and return translated text
def translate(text):
    # Store the resulting call to the "result" variable, holds 2 parameters
    result = translator.translate_text(
        text,
        # For now hardcode the source language to be Japanese, if not hardcoded is detected
        source_lang="JA",
        # Set target translated text to be returned in English, US based
        target_lang="EN-US",
    )
    # Return the resutling text string
    return result.text
