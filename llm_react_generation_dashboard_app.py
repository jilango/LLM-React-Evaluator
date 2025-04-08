import streamlit as st
import openai
import matplotlib.pyplot as plt
import nltk
from nltk.translate.bleu_score import sentence_bleu
import time

nltk.download('punkt')

openai.api_key = st.secrets["####"] if "####" in st.secrets else "####" #replace with OpenAI key

# Testing Prompts
prompts = {
    "Prompt 1": "Write a minimal React functional component based on the following description:",
    "Prompt 2": "Generate a JSX code snippet for the given UI description:",
    "Prompt 3": "Create a simple React component that matches the description below:",
    "Prompt 4": "Provide clean and minimal React (JSX) code for:",
    "Prompt 5": "Write a concise React component using hooks if needed for the following UI:",
    "Prompt 6": "Develop a simple React UI element as per the following description:",
    "Prompt 7": "Create a TypeScript React component for the given description:",
    "Prompt 8": "Write a JSX code snippet optimized for readability based on this UI description:",
    "Prompt 9": "Given the following description, build a functional React component:",
    "Prompt 10": "Generate a basic React structure in JSX to match the following UI description:",
}


def query_openai(prompt_text, input_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{prompt_text}\n{input_text}"},
            ],
            temperature=0.2,
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return ""

# App Components
st.title("\ud83d\udcca LLM React Code Generation Evaluation (Upload Files)")
st.write("Upload your description and expected code files to compare prompt performances.")

# Uploading description and expected code files
description_file = st.file_uploader("Upload Component Descriptions (.txt)", type=["txt"])
code_file = st.file_uploader("Upload Target Code (.txt)", type=["txt"])

if description_file and code_file:
    descriptions = description_file.read().decode("utf-8").strip().split("\n")
    target_codes = code_file.read().decode("utf-8").strip().split("\n")

    if len(descriptions) != len(target_codes):
        st.error("Mismatch: Number of descriptions and target codes must be equal.")
    else:
        selected_prompts = st.multiselect(
            "Choose prompt templates to evaluate:",
            list(prompts.keys()),
            default=list(prompts.keys())
        )

        if st.button("Run Evaluation"):
            st.info("Evaluating prompts. Please wait...")
            progress_bar = st.progress(0)

            results = {}
            bleu_scores = {prompt_name: [] for prompt_name in selected_prompts}
            total_steps = len(selected_prompts) * len(descriptions)
            current_step = 0

            for prompt_name in selected_prompts:
                prompt_template = prompts[prompt_name]
                generated_codes = []
                for description in descriptions:
                    code = query_openai(prompt_template, description)
                    generated_codes.append(code)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                results[prompt_name] = generated_codes

            for prompt_name, codes in results.items():
                for generated, target_code in zip(codes, target_codes):
                    reference = target_code.split()
                    candidate = generated.split()
                    bleu = sentence_bleu([reference], candidate)
                    bleu_scores[prompt_name].append(bleu)

            average_bleu = {k: sum(v)/len(v) for k, v in bleu_scores.items()}

            # Plot
            st.subheader("\ud83d\udd22 Average BLEU Score per Prompt")
            fig, ax = plt.subplots()
            ax.bar(average_bleu.keys(), average_bleu.values())
            ax.set_ylabel("Average BLEU Score")
            ax.set_ylim(0, 1)
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)

            # Table of Individual Scores
            st.subheader("\ud83d\udd22 Individual BLEU Scores")
            for prompt_name, scores in bleu_scores.items():
                st.write(f"### {prompt_name}")
                for idx, score in enumerate(scores):
                    st.write(f"Component {idx+1}: BLEU Score = {score:.2f}")


            best_prompt = max(average_bleu, key=average_bleu.get)
            st.success(f"\ud83c\udfc6 Best Performing Prompt: {best_prompt} with Avg BLEU = {average_bleu[best_prompt]:.2f}")

else:
    st.warning("Please upload both description and target code files.")


st.markdown("---")
st.markdown("Built for Scale AI Prompt Engineer Practice \ud83d\ude80")
