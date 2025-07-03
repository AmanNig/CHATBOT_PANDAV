# from langchain_ollama import ChatOllama
# from config import MODEL_NAME

# #Connect to your local LLaMA 3 model
# llm = ChatOllama(model=MODEL_NAME)

# def classify_intent(question: str) -> str:
#     prompt = (
#         "You are an intent classifier. Your job is to read a user's question and classify it into ONLY ONE of these categories:\n"
#         "- yes_no: A question that can be answered with yes or no.\n"
#         "- factual: A direct factual query requesting verifiable information, such as dates, definitions, locations, or identities (e.g., 'Who is the Prime Minister of India?', 'What is today’s date?').\n"
#         "- timeline: A question about when, how long, or timeframes.\n"
#         "- insight: A question asking for an explanation, reason, or deeper understanding.\n"
#         "- guidance: A question seeking advice, recommendation, or next steps.\n"
#         "- factual: A direct factual query requesting verifiable information, such as dates, definitions, locations, or identities (e.g., 'Who is the Prime Minister of India?', 'What is today’s date?').\n"
#         "- general: Anything else, including greetings, statements, or unclear intent.\n"
#         "\n"
#         "Any question beginning with 'Who', 'What', 'Where', 'When', 'How many', or 'How much' should be classified as factual.\n"
#         "\n"
#         "Respond with ONLY one of the category names, in all lowercase, and nothing else. Do not include any explanation, punctuation, or extra words.\n"
#         "\n"
#         "Here are some examples:\n"
#         "Q: Will I become an engineer?\n"
#         "A: yes_no\n"
#         "Q: When will I become an engineer?\n"
#         "A: timeline\n"
#         "Q: Why do people become engineers?\n"
#         "A: insight\n"
#         "Q: What should I do to become an engineer?\n"
#         "A: guidance\n"
#         "Q: Who is the Prime Minister of India?\n"
#         "A: factual\n"
#         "Q: What is the capital of France?\n"
#         "A: factual\n"
#         "Q: Where is the Taj Mahal located?\n"
#         "A: factual\n"
#         "Q: How many days are in a leap year?\n"
#         "A: factual\n"
#         "Q: Hello there!\n"
#         "A: general\n"
#         "\n"
#         "Classify this question:\n"
#         f"Q: {question}\n"
#         "A:"
#     )
    
#     response = llm.invoke(prompt)
#     intent = response.content.strip().lower()

#     valid = {"yes_no", "timeline", "insight", "guidance", "factual", "general"}
#     return intent if intent in valid else "general"
from langchain_ollama import ChatOllama
from initialize.config import MODEL_NAME
import re

# Connect to your local LLaMA 3 model
llm = ChatOllama(model=MODEL_NAME)

def classify_intent(question: str) -> str:
    # Patterns for conversational queries like greetings, how are you?
    conversational_keywords = r"\b(who are you|hi|hello|hey|good morning|good evening|how are you|how's it going|bye|goodbye|see you|what's up|good night|namaste|happy diwali|happy holi)\b"

    # Check if the question is a conversational query (greetings, pleasantries)
    if re.search(conversational_keywords, question.lower()):
        return "conversation"

    # Prompt for the rest of the intents (yes_no, timeline, insight, guidance, factual, general)
    prompt = (
        "You are an intent classifier. Your job is to read a user's question and classify it into ONLY ONE of these categories:\n"
        "-conversation**: A friendly or casual question, such as greetings, well-wishes, or general inquiries (e.g., 'How are you?', 'Hello!', 'Good morning!','Good night','Good evening')\n"
        "- yes_no: A question that can be answered with yes or no.\n"
        "- factual: A direct factual query requesting verifiable information, such as dates, definitions, locations, or identities (e.g., 'Who is the Prime Minister of India?', 'What is today’s date?').\n"
        "- timeline: A question about when, how long, or timeframes.\n"
        "- insight: A question asking for an explanation, reason, or deeper understanding.\n"
        "- guidance: A question seeking advice, recommendation, or next steps.\n"
       # "- general:  Any other question that does not fit into the above categories, including statements, vague queries, or unclear intent\n"
        "\n"
       # "Any question beginning with 'Who', 'What', 'Where', 'When', 'How many' should be classified as factual.\n"
        "\n"
        "Respond with ONLY one of the category names, in all lowercase, and nothing else. Do not include any explanation, punctuation, or extra words.\n"
        "\n"
        "Here are some examples:\n"
       " Q: 'How are you?"
       "A: 'conversation"
        "Q: Will I become an engineer?\n"
        "A: yes_no\n"
        "Q: When will I become an engineer?\n"
        "A: timeline\n"
        "Q: Why do people become engineers?\n"
        "A: insight\n"
        "Q: What should I do to become an engineer?\n"
        "A: guidance\n"
        "Q: Who is the Prime Minister of India?\n"
        "A: factual\n"
        "Q: What is the capital of France?\n"
        "A: factual\n"
        "Q: Where is the Taj Mahal located?\n"
        "A: factual\n"
        "Q: How many days are in a leap year?\n"
        "A: factual\n"
        "Q: Hello there!\n"
        "A: general\n"
        "\n"
        "Classify this question:\n"
        f"Q: {question}\n"
        "A:"
    )
    
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    # List of valid intents
    valid = {"yes_no", "timeline", "insight", "guidance", "factual", "general", "conversation"}
    
    # If intent is valid, return it, else classify as 'general'
   
    return intent if intent in valid else "general"

   
   
