# PromptCraft: React LLM Code Generation Benchmarking

PromptCraft is a lightweight benchmarking framework designed to evaluate different prompt engineering strategies for generating production-quality React frontend components using large language models (LLMs).

This project tests OpenAI’s gpt-4o model against a prebuilt set of UI component descriptions and corresponding reference React code snippets. It measures prompt effectiveness across multiple templates using BLEU scores to assess code generation accuracy and structural adherence.

## Features:

Evaluate LLM prompt performance for frontend code generation tasks.
Upload your own sets of UI descriptions and target React code.
Test across 10 customizable prompt templates.
Automatically generate model outputs and compute BLEU evaluation scores.
Visualize prompt performance through an interactive BLEU score dashboard.

## Technologies Used:

Python
OpenAI API (gpt-4o), Streamlit (frontend dashboard), NLTK (BLEU score evaluation), Matplotlib (data visualization)


## Workflow:

Upload sample descriptions and target codes, select the prompt templates to evaluate, run the benchmark, analyze BLEU scores and visualize prompt performance.
