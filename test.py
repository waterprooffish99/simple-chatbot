import google.generativeai as genai

# Put your API key here (better to use environment variable in production)
API_KEY = "AIzaSyBUkaOKpxmTi-lXZQUMRQBMMJQKXaDrENU"

# Configure the API key
genai.configure(api_key=API_KEY)

# List all models you have access to
models = genai.list_models()

print("Available models:")
for model in models:
    print(f"- {model.name}")
    # Optional: show supported generation methods
    # print(f"   Supported methods: {model.supported_generation_methods}")