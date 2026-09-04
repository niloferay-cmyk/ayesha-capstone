import asyncio

BATCH_SIZE = 5

async def run_batched_pipeline(questions: list[Question], fail_rate: float = 0.0) -> list[Answer]:
    """Processes questions in batches of BATCH_SIZE, running each batch concurrently."""
    results: list[Answer] = []

    for i in range(0, len(questions), BATCH_SIZE):
        batch = questions[i:i + BATCH_SIZE]          # exactly 5 questions (or fewer on the last batch)
        print(f"Starting batch {i // BATCH_SIZE + 1}: {len(batch)} questions")

        batch_results = await asyncio.gather(
            *(ask_llm_with_retry(q, fail_rate=fail_rate) for q in batch)
        )
        results.extend(batch_results)

        await asyncio.sleep(0.1)  # gentle pace between batches

    return results