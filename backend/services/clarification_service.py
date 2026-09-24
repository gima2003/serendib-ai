from llm.gemini_provider import client

def generate_clarification_question(
        prompt: str
) -> str:

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    return response.text.strip()