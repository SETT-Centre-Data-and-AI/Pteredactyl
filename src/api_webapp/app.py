import logging
import logging.config
from pathlib import Path

import gradio as gr
import yaml

import pteredactyl as pt

# Logging configuration. This is only done at root level
logging_config = yaml.safe_load(Path("logging.yaml").read_text())
logging.config.dictConfig(logging_config)

# Get the logger
log = logging.getLogger(__name__)

# Load the model
log.info("Starting App")

# Function to redact text
def redact(text: str):
    anonymized_text = pt.anonymise(text)
    # Replace < and > with [ and ] to avoid HTML interpretation issues
    anonymized_text = anonymized_text.replace("<", "[").replace(">", "]")
    return anonymized_text


# Function to manually flag false negatives and count them
def flag_false_negatives(text: str):
    false_negatives = {
        "Brown's": "[FALSE_NEGATIVE]Brown's[/FALSE_NEGATIVE]",
        "Kaposi Sarcoma": "[FALSE_NEGATIVE]Kaposi Sarcoma[/FALSE_NEGATIVE]",
        "Sarcoma's diagnosis": "[FALSE_NEGATIVE]Sarcoma's diagnosis[/FALSE_NEGATIVE]",
        "[PERSON] Lymphoma": "[FALSE_NEGATIVE][PERSON] Lymphoma[/FALSE_NEGATIVE]",
        "Henoch Schonlein": "[FALSE_NEGATIVE]Henoch Schonlein[/FALSE_NEGATIVE]",
        "Gehrig's": "[FALSE_NEGATIVE]Gehrig's[/FALSE_NEGATIVE]",
    }
    count = 0
    for original, replacement in false_negatives.items():
        if original in text:
            count += text.count(original)
            text = text.replace(original, replacement)
    return text, count


# Function to visualize the redaction tokens
def visualize_entities(redacted_text: str):
    colors = {
        "PERSON": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "ID": "linear-gradient(90deg, #ff9a9e, #fecfef)",
        "GPE": "linear-gradient(90deg, #fccb90, #d57eeb)",
        "NHS_NUMBER": "linear-gradient(90deg, #ff9a9e, #fecfef)",
        "NUMBER": "linear-gradient(90deg, #ff9a9e, #fecfef)",
        "DATE_TIME": "linear-gradient(90deg, #fddb92, #d1fdff)",
        "LOCATION": "linear-gradient(90deg, #a1c4fd, #c2e9fb)",
        "EVENT": "linear-gradient(90deg, #a6c0fe, #f68084)",
        "POSTCODE": "linear-gradient(90deg, #c2e59c, #64b3f4)",
        "FALSE_NEGATIVE": "linear-gradient(90deg, #ff6b6b, #ff9a9e)",  # Red for false negatives
        "/FALSE_NEGATIVE": "linear-gradient(90deg, #ff6b6b, #ff9a9e)",  # Red for false negatives
    }

    # Map of tokens to color classes
    token_colors = {
        "[PERSON]": "PERSON",
        "[LOCATION]": "LOCATION",
        "[ID]": "ID",
        "[NHS_NUMBER]": "NHS_NUMBER",
        "[NUMBER]": "NUMBER",
        "[DATE_TIME]": "DATE_TIME",
        "[EVENT]": "EVENT",
        "[POSTCODE]": "POSTCODE",
        "[FALSE_NEGATIVE]": "FALSE_NEGATIVE",
        "[/FALSE_NEGATIVE]": "/FALSE_NEGATIVE",
    }

    # Function to wrap tokens with span elements without replacing the token
    def wrap_token_in_html(text, token, color):
        parts = text.split(token)
        wrapped_token = f'<span style="background: {color}; padding: 2px; border-radius: 3px;">{token}</span>'
        return wrapped_token.join(parts)

    # Wrap each token with highlighted spans
    for token, color_class in token_colors.items():
        redacted_text = wrap_token_in_html(redacted_text, token, colors[color_class])

    return f'<div style="white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{redacted_text}</div>'


def redact_and_visualize(text: str):
    redacted_text = redact(text)
    redacted_text_with_fn, fn_count = flag_false_negatives(redacted_text)
    visualized_html = visualize_entities(redacted_text_with_fn)
    return visualized_html, f"Total False Negatives: {fn_count}"


hint = """
# Guide/Instructions

## How the tool works:

When the input text is entered, the tool redacts the entered text with labelled masking tokens.

The model running under the hood is presently: "StanfordAIMI/stanford-deidentifier-base" which can be obtained here: [Link To Stanford Model on Huggingface](https://huggingface.co/StanfordAIMI/stanford-deidentifier-base)

### Strengths
- The tool is 99% accurate on our test set of radiology reports.

### Limitations
- The tool was not designed initially to redact clinic letters as it was developed primarily on radiology reports.

- It's known significant weaknesses are that it misses postcodes as these were not in its development set.

- It may overly aggressively redact text because it was built as a research tool where precision is prized > recall.
"""

sample_text = """
1. Dr. Huntington (NHS No: 1234567890) diagnosed Ms. Alzheimer with Alzheimer's disease during her last visit to the Huntington Medical Center on 12/12/2023. The prognosis was grim, but Dr. Huntington assured Ms. Alzheimer that the facility was well-equipped to handle her condition despite the lack of a cure for Alzheimer's.

2. Paget Brewster (NHS No: 0987654321), a 45-year-old woman, was recently diagnosed with Paget's disease of bone by her physician, Dr. Graves at St. Jenny's Hospital on 01/06/2026 Postcode: JE30 6YN. Paget's disease is a chronic disorder that affects bone remodeling, leading to weakened and deformed bones. Brewster's case is not related to Grave's disease, an autoimmune disorder affecting the thyroid gland.

3. Crohn Marshall (NHS No: 943 476 5918), a 28-year-old man, has been battling Crohn's disease for the past five years. Crohn's disease is a type of inflammatory bowel disease (IBD) that causes inflammation of the digestive tract. Marshall's condition is managed by his gastroenterologist, Dr. Ulcerative Colitis, who specializes in treating IBD patients at the Royal Free Hospital.

4. Addison Montgomery (NHS No: 5566778899), a 32-year-old woman, was rushed to University College Hospital on 18/09/2023 after experiencing severe abdominal pain and fatigue. After a series of tests, Dr. Cushing diagnosed Montgomery with Addison's disease, a rare disorder of the adrenal glands. Postcode is NH77 9AF. Montgomery's condition is not related to Cushing's syndrome, which is caused by excessive cortisol production.

5. Lou Gehrig (NHS No: 943 476 5919), a renowned baseball player, was diagnosed with amyotrophic lateral sclerosis (ALS) in 1939 at the Mayo Clinic. ALS, also known as Lou Gehrig's disease, is a progressive neurodegenerative disorder that affects nerve cells in the brain and spinal cord. Gehrig's diagnosis was confirmed by his neurologist, Dr. Bell, who noted that the condition was not related to Bell's palsy, a temporary facial paralysis.

6. Parkinson Brown (NHS No: 3344556677), a 62-year-old man, has been living with Parkinson's disease for the past decade. Parkinson's disease is a neurodegenerative disorder that affects movement and balance. Brown's condition is managed by his neurologist, Dr. Lewy Body, who noted that Brown's symptoms were not related to Lewy body dementia, another neurodegenerative disorder, at King's College Hospital.

7. Kaposi Sarcoma (NHS No: 9988776655), a 35-year-old man, was recently diagnosed with Kaposi's sarcoma, a type of cancer that develops from the cells that line lymph or blood vessels, at Guy's Hospital on 17/04/2023. Sarcoma's diagnosis was confirmed by his oncologist, Dr. Burkitt Lymphoma, who noted that the condition was not related to Burkitt's lymphoma, an aggressive form of non-Hodgkin's lymphoma. He died on 17/04/2023.

8. Dr. Kawasaki (NHS No: 2233445566) treated young Henoch Schonlein for Henoch-Schönlein purpura, a rare disorder that causes inflammation of the blood vessels, at Great Ormond Street Hospital on 05/05/2024. Schonlein's case was not related to Kawasaki disease, a condition that primarily affects children and causes inflammation in the walls of medium-sized arteries.

9. Wilson Menkes (NHS No: 943 476 5915), a 42-year-old man, was diagnosed with Wilson's disease, a rare genetic disorder that causes copper to accumulate in the body. Menkes' diagnosis was confirmed by his geneticist, Dr. Niemann Pick, at Addenbrooke's Hospital on 02/02/2025, who noted that the condition was not related to Niemann-Pick disease, another rare genetic disorder that affects lipid storage. Postcode was GH75 3HF.

10. Dr. Marfan (NHS No: 4455667788) treated Ms. Ehlers Danlos for Ehlers-Danlos syndrome, a group of inherited disorders that affect the connective tissues, at the Royal Brompton Hospital on 30/11/2024. Danlos' case was not related to Marfan syndrome, another genetic disorder that affects connective tissue development and leads to abnormalities in the bones, eyes, and cardiovascular system.
"""

description = """
*Release Date:* 29/06/2024

*Version:* **1.0** - Working Proof of Concept Demo with API option

*Authors:* **Cai Davis, Michael George, Matt Stammers**
"""

iface = gr.Interface(
    fn=redact_and_visualize,
    inputs=gr.Textbox(value=sample_text, label="Input Text", lines=25),
    outputs=[
        gr.HTML(label="Anonymised Text with Visualization"),
        gr.Textbox(label="Total False Negatives", lines=1),
    ],
    title="SETT: Data and AI. Pteredactyl Demo",
    description=description,
    article=hint,
)

iface.launch(server_name="0.0.0.0", server_port=7801)
