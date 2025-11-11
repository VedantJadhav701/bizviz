"""
Quick test to verify Groq API key is working
"""
import os
from groq import Groq

# Try loading from environment
api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    # Try loading from secrets file
    try:
        with open('.streamlit/secrets.toml', 'r') as f:
            content = f.read()
            if 'GROQ_API_KEY' in content:
                # Extract key
                for line in content.split('\n'):
                    if 'GROQ_API_KEY' in line and '=' in line:
                        api_key = line.split('=')[1].strip().strip('"').strip("'")
                        break
    except Exception as e:
        print(f"Error reading secrets: {e}")

print(f"API Key found: {'Yes' if api_key else 'No'}")
print(f"API Key (first 20 chars): {api_key[:20] if api_key else 'N/A'}...")

if api_key:
    try:
        print("\n🧪 Testing Groq API connection...")
        client = Groq(api_key=api_key)
        
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": "Say 'Hello, API is working!' in exactly 5 words."
            }],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        print("\n✅ SUCCESS: Groq API is working correctly!")
        
    except Exception as e:
        print(f"❌ ERROR: Groq API test failed: {e}")
else:
    print("\n❌ ERROR: No API key found!")
    print("\nTo fix:")
    print("1. Check .streamlit/secrets.toml exists")
    print("2. Verify it contains: GROQ_API_KEY = \"your_key_here\"")
    print("3. Or set environment variable: $env:GROQ_API_KEY=\"your_key\"")
