import google.generativeai as genai
genai.configure(api_key="AIzaSyB_V9KsP7iRsQWpTZowOi0Bou0vJ8yDlJM")


print("Available generateContent models:")
for m in genai.list_models():
    if "generateContent" in getattr(m, "supported_generation_methods", []):
        print(m.name)