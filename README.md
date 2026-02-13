# RAG Tutorial 07 — Parent-Document Retrieval

<p align="center">
  <a href="https://github.com/BellaBe/mastering-rag"><img src="https://img.shields.io/badge/Series-Mastering_RAG-blue?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/Part-7_of_16-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" />
</p>

> **Part of the [Mastering RAG](https://github.com/BellaBe/mastering-rag) tutorial series**  
> Previous: [06 — Wikipedia Chatbot](https://github.com/BellaBe/rag-06-wikipedia-chatbot) | Next: [08 — Query Rewriting](https://github.com/BellaBe/rag-08-query-rewriting)

---

## Real-World Scenario

> A medical Q&A system indexes clinical guidelines. A doctor asks: "What's the recommended dosage for metformin in elderly patients with renal impairment?" Standard RAG retrieves a small chunk: *"adjust dose for renal function."* Helpful, but missing the full picture. **Parent-document retrieval** matches on that precise sentence, then expands to the full section: dosage tables, contraindications, monitoring requirements. The doctor gets the complete clinical guidance, not just a fragment.

---

## What You'll Build

A RAG system that uses **small child chunks for precise retrieval** and **larger parent sections for rich LLM context**. Children are linked to parents via metadata, so precise vector matches expand into coherent context blocks.

```
Standard RAG:             Parent-Document RAG:
┌───────────┐             ┌───────────┐
│ Small     │  retrieve   │ Small     │  retrieve      ┌──────────────┐
│ chunk     │  ──→ LLM    │ child     │  ──→ expand ──→│ Large parent │──→ LLM
│ = context │             │ chunk     │                 │ section      │
└───────────┘             └───────────┘                 └──────────────┘
Less context              Precise match                  Rich context
```

## Key Concepts

- **Parent-child hierarchy**: documents split at two granularities
- **Precision vs. context trade-off**: small chunks match better, large chunks explain better
- **Metadata linking**: each child stores a reference to its parent
- **Context expansion**: retrieve children, return parents to the LLM

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+ · FastAPI · ChromaDB · Sentence-Transformers · OpenAI |
| Frontend | React 19 · Vite · Tailwind CSS |

## Quick Start

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8003
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — ingest documents, query, and inspect child vs. parent chunks.

## What You'll Learn

1. Why the best retrieval chunk size differs from the best generation chunk size
2. How to implement parent-child chunking and metadata linking
3. When parent-document retrieval outperforms standard RAG
4. How to visualize and debug the child → parent expansion

## Prerequisites

- Python 3.11+ and Node.js 18+
- Concepts from [Tutorial 05](https://github.com/BellaBe/rag-05-basic-rag-pipeline) (basic RAG pipeline)
- Understanding of chunking from [Tutorial 02](https://github.com/BellaBe/rag-02-chunking-strategies)

## Exercises

1. **Size experiment**: Try child sizes of 100, 200, 500 chars and parent sizes of 500, 1000, 2000 chars. What combination gives the best answers for your documents?
2. **Overlap children**: Add overlap to child chunks. Does it improve retrieval, or does parent expansion already handle boundary issues?
3. **Multiple children, same parent**: Ask a query that matches 3 children from the same parent. Does the system deduplicate and return the parent once, or three times?
4. **A/B comparison**: Run 10 queries with standard RAG and parent-doc RAG side by side. Count how many times each approach gives a better answer.
5. **Hierarchical parents**: Implement 3 levels: sentence → paragraph → section. When would you want to expand to paragraph vs. full section?

## Common Mistakes

| Mistake | Why It Happens | How to Fix |
|---------|---------------|------------|
| Parent context is too large for LLM | Parent chunks set to entire pages or sections | Cap parent size at ~1000–2000 tokens; split large sections further |
| Child-to-parent link is broken | Metadata mapping error during ingestion | Validate links at ingestion time: every child must have a valid parent_id |
| Duplicate parents in context | Multiple children from the same parent all get expanded | Deduplicate parents before sending to the LLM |
| Child chunks too small to be meaningful | Set to 50 chars for "maximum precision" | Keep children at 100–200 chars minimum so embeddings have enough signal |

## Further Reading

- [LangChain ParentDocumentRetriever](https://python.langchain.com/docs/how_to/parent_document_retriever/) — Framework implementation of this pattern
- [Small-to-Big Retrieval](https://docs.llamaindex.ai/en/stable/examples/retrievers/auto_merging_retriever/) — LlamaIndex's approach (auto-merging retriever)
- [Retrieval Strategies Compared](https://www.rungalileo.io/blog/mastering-rag-advanced-chunking-techniques-for-llm-applications) — Advanced chunking patterns

## Next Steps

Head to **[Tutorial 08 — Query Rewriting & Expansion](https://github.com/BellaBe/rag-08-query-rewriting)** to improve what happens _before_ retrieval — making the query itself better.

---

<p align="center">
  <sub>Part of <a href="https://github.com/BellaBe/mastering-rag">Mastering RAG — From Zero to Production</a></sub>
</p>
