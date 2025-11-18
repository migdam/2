from openai import OpenAI

client = OpenAI()

EXPLANATION_PROMPT = """
You are an expert in organizational strategy mapping.

Given:
- Text: <<<TEXT>>>
- Strategy: <<<STRATEGY>>>
- Similarity Score: <<<SCORE>>>

Explain in 2–4 sentences **why** this text aligns with this strategy.
Do not mention embeddings, cosine similarity, or technical details.
Show the strategic logic clearly.
"""

def explain_alignment(text, strategy_name, score):
    prompt = EXPLANATION_PROMPT \
        .replace("<<<TEXT>>>", text) \
        .replace("<<<STRATEGY>>>", strategy_name) \
        .replace("<<<SCORE>>>", str(round(score, 3)))

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp.choices[0].message.content
