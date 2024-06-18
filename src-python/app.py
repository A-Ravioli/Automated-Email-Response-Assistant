# app.py
from flask import Flask, request, jsonify
from transformers import pipeline
from langchain.chains import SimpleSequentialChain
from langchain.llms import GPT2LMHeadModel
from langchain.prompts import SimplePromptTemplate

app = Flask(__name__)

# Load lightweight models for local inference
classifier = pipeline("text-classification", model="distilbert-base-uncased")
generator = pipeline("text-generation", model="gpt2")


# Define a simple prompt template for generating responses
class EmailResponsePromptTemplate(SimplePromptTemplate):
    def __init__(self):
        template = "Generate a polite response to the following email: {email}"
        super().__init__(template)


# Define the classification and response generation steps
def classify_email_step(email_content):
    classification = classifier(email_content)[0]["label"].lower()
    return classification


def generate_response_step(email_content):
    prompt = EmailResponsePromptTemplate()
    response_text = generator(prompt.format(email=email_content), max_length=100)[0][
        "generated_text"
    ]
    return response_text


# Combine the steps into a sequential chain
email_analysis_chain = SimpleSequentialChain(
    [classify_email_step, generate_response_step]
)


@app.route("/analyze", methods=["POST"])
def analyze_email():
    data = request.get_json()
    email_content = data["email"]

    # Run the email through the agentic chain
    classification = classify_email_step(email_content)

    if classification == "neutral":  # Assuming 'neutral' means it can be handled by AI
        response_text = generate_response_step(email_content)
    else:
        response_text = "This email requires your attention."

    return jsonify({"response": response_text})


if __name__ == "__main__":
    app.run(debug=True)
