import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from pypdf import PdfReader,PdfWriter # type: ignore
from user.models import Student
import openai # type: ignore

def generate_certificate(user, quiz, score, passed, date_attempted):
    # Select the template based on whether the user passed or failed the quiz
    template_filename = 'certificate_e.pdf' if passed else 'certificate_c.pdf'
    
    # Create a temporary PDF with user details to overlay on the template
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 22)
    
    student=Student.objects.get(user=user)
    student_name=student.name
    
    # Draw text onto the temporary PDF
    c.drawString(400, 410, f"{student_name}")
    c.drawString(390, 342, f"{quiz.grade}")
    c.drawString(400, 290, f"{quiz.quiz_name}")  # Assuming quiz_name is the correct field
    c.drawString(420, 236, f"{score:.2f}%")
    c.drawString(405, 157, f"{date_attempted.strftime('%d-%m-%Y')}")
    
    c.save()
    buffer.seek(0)

    # Load the template PDF
    template_path = os.path.join(settings.MEDIA_ROOT, template_filename)
    template_reader = PdfReader(template_path)
    template_writer = PdfWriter()
    
    # Overlay the content on the template PDF
    template_page = template_reader.pages[0]
    overlay_pdf = PdfReader(buffer)
    overlay_page = overlay_pdf.pages[0]
    
    template_page.merge_page(overlay_page)
    template_writer.add_page(template_page)

    # Save the final PDF to a buffer
    final_buffer = BytesIO()
    template_writer.write(final_buffer)
    final_buffer.seek(0)
    
    # Create a ContentFile for saving
    filename = f"{user.username}_{quiz.quiz_name}_certificate.pdf"
    return ContentFile(final_buffer.getvalue(), filename)

# Set up your OpenAI API Key (for example, in your settings.py)
openai.api_key = settings.OPENAI_API_KEY  # Store your key securely

def generate_questions_and_answers_using_ai(quiz_name, no_of_questions, topic):
    # Use ChatCompletion instead of Completion
    messages = [
        {
            "role": "system",
            "content": (
                "You are an educational AI assistant. Generate a quiz with "
                f"{no_of_questions} questions and their answers based on the topic '{topic}'. "
                "Provide each question as a key and its correct answer as the value in JSON format."
            ),
        },
        {
            "role": "user",
            "content": f"Generate {no_of_questions} questions for a quiz named '{quiz_name}' on the topic '{topic}'.",
        },
    ]
    
    questions = []
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )
        
         # Log the raw response for debugging
        print("OpenAI Response:", response)
        # Extract the response content
        generated_text = response['choices'][0]['message']['content']
        print("Generated Text:", generated_text)
        # generated_text = response['choices'][0]['text']
        for q_and_a in generated_text.split("\n\n"):
            if not q_and_a.strip():
                continue
            question_part, *answers_part = q_and_a.split("\n")
            question = question_part.split(": ", 1)[-1]
            answers = []
            correct_answer = None
            for answer in answers_part:
                if answer.startswith("*"):  # Indicating the correct answer
                    correct_answer = answer.strip("* ").strip()
                    answers.append(correct_answer)
                else:
                    answers.append(answer.strip())
            questions.append({"question": question, "answers": answers, "correct": correct_answer})
    except openai.OpenAIError as e:
        print(f"Error with OpenAI API: {e}")
        return []
    return questions