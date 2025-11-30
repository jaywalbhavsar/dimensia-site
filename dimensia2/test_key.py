import google.generativeai as genai

# PASTE YOUR KEY HERE INSIDE THE QUOTES
# It must start with "AIza"
TEST_KEY = "AIzaSyChMOdqn6zWuj6IzdxzLogvyKQplnaM6UY"

print(f"Testing Key: {TEST_KEY}...")

try:
    genai.configure(api_key=TEST_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print("\n✅ SUCCESS! The Key works.")
    print(f"AI Response: {response.text}")
except Exception as e:
    print("\n❌ FAIL! The Key is still wrong.")
    print(f"Error Message: {e}")