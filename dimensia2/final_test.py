import google.generativeai as genai

# PASTE YOUR KEY HERE
TEST_KEY = "AIzaSyChMOdqn6zWuj6IzdxzLogvyKQplnaM6UY"

print(f"Testing Key with 'gemini-pro'...")

try:
    genai.configure(api_key=TEST_KEY)
    
    # We are using 'gemini-pro' because it is the most compatible model
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content("Write a short tagline for a design agency.")
    
    print("\n✅ SUCCESS! Your API Key works perfectly.")
    print(f"AI Response: {response.text}")
    print("\nIMPORTANT: Make sure your app.py uses 'gemini-pro' on line 30!")
    
except Exception as e:
    print("\n❌ ERROR DETAILS:")
    print(e)