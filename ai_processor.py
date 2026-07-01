from google import genai

client = genai.Client(
    api_key=""
)

def generate_summary(text):

    prompt = f"""
    Summarize this research paper:

    {text[:10000]}
    """

    response = client.models.generate_content(
        model="",
        contents=prompt
    )

    return response.text