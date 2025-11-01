import os
from dotenv import load_dotenv
from PIL import Image
from _modules.utility_openai import generate_questions_from_image, DEFAULT_AI_LLM_MODEL
from _modules.utility_pdfs_images import convert_pdf_doc_to_image


LLM_PROMPT_PREPARE_QUIZ = ("You are an expert quiz creator. preparing a quiz for students based on the content of the image provided. "
                           " the quiz should consist of multiple-choice questions that test comprehension and critical thinking skills. "
                           " Each question should have four options, labeled A, B, C, and D, with one correct answer. "
                           " Ensure that the questions cover key concepts and details from the image. "
                           " provide the expected answers after each question. "
                           " limit to only 3 questions. ")

def main():
    
    load_dotenv()

    convert_pdf_doc_to_image("data-workspace/Physics-WEB_Sab7RrQ.pdf", 
                             "data-workspace/Physics-Section-Acceleration.png", 
                             from_page=108, to_page=109, dpi=300)
    image_path = "data-workspace/Physics-Section-Acceleration.png"  


    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    llm_model = os.getenv("USE_AI_LLM_MODEL", DEFAULT_AI_LLM_MODEL)

    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        return

    
    # Check if a placeholder image exists, if not create one.
    if not os.path.exists(image_path):
        print(f"Creating a placeholder image named '{image_path}'.")
        try:
            img = Image.new('RGB', (200, 100), color = 'red')
            img.save(image_path, 'PNG')
            print("Placeholder image created. Replace it with your actual image.")
        except Exception as e:
            print(f"Could not create a placeholder image: {e}")
            return
    
    print(f"Analyzing image: {image_path}")
    questions = generate_questions_from_image(api_key, base_url, image_path, LLM_PROMPT_PREPARE_QUIZ, llm_model)
    print("\n--- Generated Questions ---")
    print(questions)
    print("---------------------------\n")


if __name__ == "__main__":
    main()
