from __future__ import annotations
import sys

import asyncio
import random
from dataclasses import dataclass

@dataclass
class Question:
    text: str


@dataclass
class Answer:
    text: str
    
class TransientError(Exception):
    """Raised by fake_ask_llm to simulate transient failures."""
    pass

async def fake_llm(question,fail_rate):
    if random.random() < fail_rate :
            await asyncio.sleep(0.1) 
            raise TransientError("simulated transient failure")
    await asyncio.sleep(random.uniform(0.3, 1.5))
    return Answer(text=f"Stub answer for: {question[:40]}")
    
async def ask_llm_retry(question,fail_rate,max_attempts: int = 3) -> Answer:
    for attempt in range(max_attempts):
            try:
                return await fake_llm(question, fail_rate=fail_rate)
            except TransientError:
                if attempt == max_attempts - 1:
                    raise
                backoff_seconds = 2 ** attempt  # 1, 2, 4
                await asyncio.sleep(backoff_seconds)
            raise RuntimeError("unreachable")

async def run_batch_stream(questions,fail_rate: float = 0.0):
    print(questions)
    tasks=[]
    results=[]
    for q in questions:
        print(q)
        answer =  ask_llm_retry(q,fail_rate)
        tasks.append(answer)
        print(tasks)
    for c in asyncio.as_completed(tasks):
            ans = await c
            print(f"  ✓ {ans.text[:60]}...")  # arrives the instant it's ready
            results.append(ans)
    return results
       

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        fail_rate = float(sys.argv[1])
    else :
        fail_rate = 0.0
    Question = [ "What is RAG in one sentence?",
            "Name three uses of vector databases.",
            "Why might an LLM hallucinate?",
            "Explain async and await in plain language.",
            "What is the difference between a chatbot and an agent?",]
    print(Question)
    print(f"run batch stream fail_rate={fail_rate}")
    answer = asyncio.run(run_batch_stream(Question,fail_rate=fail_rate))
