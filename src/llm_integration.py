import requests
import json  # Import the json module
from config import GEMINI_API_KEY, GEMINI_ENDPOINT

def generate_email_response_gemini(prompt, context=""):
    """
    Use Gemini's API to generate a draft email response.
    Adjust the request parameters based on Gemini's documentation.
    """
    contents = [
        {
            "parts": [
                {
                    "text": f"Context: {context}\nPrompt: {prompt}"
                }
            ]
        }
    ]

    data = {
        "contents": contents,
        "generationConfig": {
            "maxOutputTokens": 150,
            "temperature": 0.7
        }
    }

    # Convert the data to JSON format
    json_data = json.dumps(data)


    response = requests.post(GEMINI_ENDPOINT, headers={"Content-Type": "application/json"}, data=json_data)

    try:
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        output = response.json()


        # Parse the response based on the actual Gemini API response structure.  This is CRITICAL!
        try:
            text = output['candidates'][0]['content']['parts'][0]['text'].strip()
        except (KeyError, IndexError) as e:
            print(f"Error parsing response: {e}")
            print(f"Full response: {output}") #DEBUG PRINT
            return "Error: Could not parse response from Gemini. Check the response structure and your code."

        return text


    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Print the error message
        print(f"Response content: {response.content}") # print the whole response for debugging
        return f"Error: Request failed - {e}. Check your network and API endpoint."

if __name__ == '__main__':
    # Example Usage:
    test_prompt = "Draft a reply to schedule a meeting next week."
    context = "Email from John: 'Can we meet next week to discuss the project?'"
    result = generate_email_response_gemini(test_prompt, context)
    print(result)