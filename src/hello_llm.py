import os, sys
from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from the environment — never hard-code keys
load_dotenv()
client = OpenAI()

def ask(question):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are concise."},
            {"role": "user",   "content": question},
        ],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "Say hello."
    answer = ask(q)
    print(answer)

    os.makedirs("docs/runs", exist_ok=True)

    with open("docs/runs/03-vector-db-uses.txt", "w", encoding="utf-8") as f:
        f.write(f"Question:\n{q}\n\n")
        f.write(f"Answer:\n{answer}\n")