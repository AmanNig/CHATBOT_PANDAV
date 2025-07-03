# core/tarot_reader.py

import random
import datetime
from langchain_ollama import ChatOllama
from initialize.config import MODEL_NAME
from utils.deck import FULL_DECK, NUMERIC_CARDS, DATE_RANGES
from core.rag import get_card_meaning
from utils.factual import answer_factual
from typing import List, Dict, Any

llm = ChatOllama(model=MODEL_NAME)

SYSTEM_PROMPT = """You are TarotTara, a friendly and empathic tarot reader.
You remember the last few messages and speak in a warm, conversational tone.
Feel free to ask clarifying questions or reference earlier points."""

def _build_history_block(history: List[Dict[str, Any]]) -> str:
    """
    Convert the conversation history (list of entries with 'question' and 'result')
    into a chat-like block:
      User: <question>
      Assistant: <interpretation>
    """
    lines = []
    for entry in history:
        q = entry.get('question', '')
        interp = entry.get('result', {}).get('interpretation', '')
        # only include if both exist
        if q:
            lines.append(f"User: {q}")
        if interp:
            lines.append(f"Assistant: {interp}")
    return "\n".join(lines)

def perform_reading(
    question: str,
    intent: str,
    history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    try:
        today = datetime.date.today()
        today_str = today.strftime('%B %d, %Y')

        # Serialize past turns
        hist_block = _build_history_block(history)

        # 1) Conversational questions
        if intent == "conversation":
            prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

Assistant:"""
            reply = llm.invoke(prompt).content.strip()
            return {"interpretation": reply, "card": None, "date_range": None}

        # 2) Factual questions: polite refusal
        if intent == "factual":
            polite = (
                "Sorry, I cannot provide factual information at the moment. "
                "Please ask a tarot-related question."
            )
            return {"interpretation": polite, "card": None, "date_range": None}

        # 3) Timeline readings
        if intent == "timeline":
            card = random.choice(NUMERIC_CARDS)
            dr = DATE_RANGES[card]
            meaning = get_card_meaning(card)
            start_str = dr[0].strftime('%B %d, %Y')
            end_str   = dr[1].strftime('%B %d, %Y')

            prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

You drew: {card}  ({start_str} – {end_str})
Meaning: {meaning}

Assistant:"""
            reply = llm.invoke(prompt).content.strip()
            return {"card": card, "date_range": dr, "interpretation": reply}

        # 4) General 3-card spread (yes_no, guidance, insight, or general)
        cards = random.sample(FULL_DECK, k=3)
        meanings = [get_card_meaning(c, k=1) for c in cards]

        prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

Cards drawn:
1. {cards[0]} — {meanings[0]}
2. {cards[1]} — {meanings[1]}
3. {cards[2]} — {meanings[2]}

Assistant:"""
        reply = llm.invoke(prompt).content.strip()
        return {"cards": cards, "interpretation": reply}

    except Exception as e:
        return {"error": str(e)}


