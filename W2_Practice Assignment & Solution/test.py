from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass

print(random.random())
@dataclass
class Question:
    text: str


@dataclass
class Answer:
    text: str
    
class TransientError(Exception):
    """Raised by fake_ask_llm to simulate transient failures."""
    pass

async def fake_ask_llm(question: Question, fail_rate: float = 0.0) -> Answer:
    """Simulates an LLM call. Sleeps for a random 0.3-1.5s, may fail."""
    if random.random() < fail_rate:
        await asyncio.sleep(0.1)  # small delay before failing
        raise TransientError("simulated transient failure")
    await asyncio.sleep(random.uniform(0.3, 1.5))
    # Return a stub answer that includes the question for visibility
    return Answer(text=f"Stub answer for: {question.text[:40]}")

async def ask_llm_with_retry(question: Question, fail_rate: float = 0.0,
                              max_attempts: int = 3) -> Answer:
    """Wraps fake_ask_llm with 1s/2s/4s backoff on transient failures."""
    for attempt in range(max_attempts):
        try:
            return await fake_ask_llm(question, fail_rate=fail_rate)
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            backoff_seconds = 2 ** attempt  # 1, 2, 4
            await asyncio.sleep(backoff_seconds)
    raise RuntimeError("unreachable")

async def run_batch(questions: list[Question],
                     fail_rate: float = 0.0) -> list[Answer]:
    """All-or-nothing: returns when slowest call finishes, in input order."""
    tasks = [ask_llm_with_retry(q, fail_rate=fail_rate) for q in questions]
    return await asyncio.gather(*tasks)

async def run_batch_stream(questions: list[Question],
                            fail_rate: float = 0.0) -> list[Answer]:
    """Streams: prints each answer as it arrives, returns in completion order.

    Use this when you want to start processing as results stream in,
    or to see which calls are slow vs fast. Don't use this when input
    order matters in the returned list.
    """
    tasks = [ask_llm_with_retry(q, fail_rate=fail_rate) for q in questions]
    results: list[Answer] = []
    for coro in asyncio.as_completed(tasks):
        ans = await coro
        print(f"  ✓ {ans.text[:60]}...")  # arrives the instant it's ready
        results.append(ans)
    return results


if __name__ == "__main__":
    import sys
    fail_rate = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    
    # sample = [Question(text=t) for t in [
    #         "What is RAG in one sentence?",
    #         "Name three uses of vector databases.",
    #         "Why might an LLM hallucinate?",
    #         "Explain async and await in plain language.",
    #         "What is the difference between a chatbot and an agent?",
    #     ]]
    # print(sample)
    Questions =["What is RAG in one sentence?",
            "Name three uses of vector databases.",
            "Why might an LLM hallucinate?",
            "Explain async and await in plain language.",
            "What is the difference between a chatbot and an agent?"]
    
    for t in Questions:
        sample=[Question(text=t)]
        #print(sample)
        answers = asyncio.run(run_batch_stream(sample, fail_rate=fail_rate))
        print(f"\nreturned {len(answers)} answers")