from fastapi import APIRouter
from pydantic import BaseModel
import json

from app.logic.intent_extractor import extract_intent
from app.rag.retriever import retrieve_phones
from app.logic.comparator import compare_phones
from app.core.safety import is_safe
from app.logic.llm import generate_response
from app.logic.response_builder import build_response

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat(req: ChatRequest):

    # ---------------- Safety ----------------
    safety = is_safe(req.message)

    if not safety["allowed"]:
        if safety["reason"] == "security":
            return {
                "message": "I can help with mobile phone recommendations, but I can’t assist with that request.",
                "intent": "blocked",
                "recommendations": [],
                "results": []
            }

        if safety["reason"] == "out_of_domain":
            return {
                "message": "I’m designed to help with mobile phone recommendations and comparisons. Please ask something related to phones.",
                "intent": "out_of_domain",
                "recommendations": [],
                "results": []
            }


    # ---------------- Intent ----------------
    intent = extract_intent(req.message)
    # print("Extracted Intent:", intent)
    # ---------------- Retrieval ----------------
    phones = retrieve_phones(
        budget=intent["budget"],
        brands=intent["brands"],
        use_cases=intent["use_cases"],
        k=intent["max_results"]
    )

    if not phones:
        return {
            "message": "I couldn’t find suitable phones for your request.",
            "intent": "recommendation",
            "recommendations": [],
            "results": []
        }

    # ---------------- Comparison vs Recommendation ----------------
    if intent["comparison"]:
        # print(phones)
        llm_input = compare_phones(phones)
    else:
        llm_input = phones

    # ---------------- LLM (language only) ----------------
    # print("LLM Input:", llm_input)
    llm_raw = generate_response(req.message, llm_input)
    llm_data = json.loads(llm_raw)

    message = llm_data.get("message", "Here are some phone recommendations for you:")
    reasons = llm_data.get("reasons", [])

    # ---------------- Canonical Response ----------------
    return build_response(
        message=message,
        phones=phones,
        reasons=reasons
    )
