# Ayesha-Capstone — Knowledge Assistant

A 30-week build of a Q&A assistant over a small document corpus,
completed as part of
the *Agentic AI & RAG Engineering* programme.

## Corpus

HR policies
(employee handbook, leave policy, benefits guide).
Product manuals
(a small set of technical product PDFs).
Public regulatory PDFs
(a SEBI / RBI / GDPR document set).
Open-source project documentation
(e.g. FastAPI, LangChain, NumPy docs).
Constraints (these matter — re-read slide 14 if needed):
5 to 20 documents —
not
hundreds.
No real PII or confidential data.
If you'd hesitate to let a peer review the corpus, swap it.
Source must be reachable — if it's behind a login, swap it.

My capstone corpus: FastAPI documentation (5 pages: tutorial intro, dependencies,security, testing, deployment). Source: https://fastapi.tiangolo.com/

## Structure

- `src/` — application code
- `docs/adr/` — Architecture Decision Records (one per major design
  choice)
- `docs/runs/` — saved LLM outputs for evidence and reference

## Week 1

- [x] Set up repo + secrets discipline
- [ ] Build `hello_llm.py` (Lab Step 2)
- [ ] Write ADR v1 (Lab Step 3)