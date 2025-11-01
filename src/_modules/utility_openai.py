from openai import OpenAI
from .utility_pdfs_images import encode_image_to_base64

DEFAULT_AI_LLM_MODEL = "qwen2.5vl:32b"  # or "llava" for Ollama

def generate_questions_from_image(api_key, base_url, image_path, prompt, llm_model=DEFAULT_AI_LLM_MODEL):
    """
    Analyzes an image and generates questions using an OpenAI-compatible API.

    Args:
        api_key (str): The API key for the LLM service.
        base_url (str): The base URL for the LLM service.
        image_path (str): The path to the image file.
        prompt (str): The prompt to guide the question generation.

    Returns:
        str: The generated questions or an error message.
    """
    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return "Could not process the image."

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=llm_model,  # Or another multi-modal model like 'llava' for Ollama
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while communicating with the API: {e}"
