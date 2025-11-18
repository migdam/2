from openai import OpenAI

client = OpenAI()

SUMMARY_PROMPT = """
You are an expert in strategic analysis and organizational transformation.

Given the following analyzed chunks:

<<<DATA>>>

Provide a structured Executive Summary with:
1. Overall Summary (5 sentences)
2. Key Strategic Alignments
3. Missed Opportunities
4. Risks / Gaps
5. Recommendations
"""

def generate_summary(chunks):
    """
    Generate an executive summary based on analyzed chunks.

    chunks = [
        {
            "text": ...,
            "best": ...,
            "score": ...,
            "explanation": ...
        }
    ]
    """
    serialized = ""
    for i, ch in enumerate(chunks, start=1):
        serialized += f"\n--- Chunk {i} ---\n"
        serialized += f"Text: {ch['text'][:200]}...\n" if len(ch['text']) > 200 else f"Text: {ch['text']}\n"
        serialized += f"Best Match: {ch['best']} (Score: {ch['score']:.3f})\n"
        serialized += f"Explanation: {ch['explanation']}\n"

    prompt = SUMMARY_PROMPT.replace("<<<DATA>>>", serialized)

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return resp.choices[0].message.content
