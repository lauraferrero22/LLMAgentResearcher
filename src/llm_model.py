import openai
import os
import truststore
truststore.inject_into_ssl()
# Set the API key and model name
MODEL = "gpt-4o-mini"
API_KEY = os.environ.get("OPENAI_API_KEY", "API KEY")


# Initialize OpenAI client
client = openai.OpenAI(api_key=API_KEY)


class LLMQuery:
    def __init__(self, prompt: str):
        self.prompt = prompt  # Store prompt at initialization

    def run(self, pdf_text: str) -> list:
        """Query the OpenAI API using the provided prompt and return structured biochar details."""
        system_message = "You are a helpful assistant. Extract and format the requested details clearly from the provided text."

        try:
            # Call OpenAI API to get a response
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"{self.prompt}\n\nText: {pdf_text}"}
                ]
            )

            # Extract response text and clean up formatting
            response_text = completion.choices[0].message.content.strip()

            
            return response_text

        except openai.OpenAIError as e:
            print(f"OpenAI API Error: {e}")
            return ""
