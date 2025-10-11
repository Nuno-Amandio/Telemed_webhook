from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/symptom-chat")
async def symptom_chat(request: Request):
    data = await request.json()
    user_message = data.get("user_message", "")
    from_number = data.get("from", "")

    prompt = f"""
    You are a helpful medical triage assistant.
    The user says: "{user_message}".
    1. Ask one short follow-up question related to their symptoms (e.g., "Are you experiencing nausea?" or "Do you have a fever?").
    2. Do NOT give diagnosis or treatment.
    3. Use plain language.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical triage assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content.strip()
    return {"result": reply, "continue": True}
