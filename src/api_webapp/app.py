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


def redact(text: str):
    anonymized_text = pt.anonymise(text)
    return anonymized_text


hint = """

# Guide/Instructions

## How the tool works:

When the input text is entered, the tool readacts the entered text with labelled masking tokens.

The model running under the hood is presently: "StanfordAIMI/stanford-deidentifier-base" which can be obtained here: [Link To Stanford Model on Huggingface](https://huggingface.co/StanfordAIMI/stanford-deidentifier-base)

### Strengths
- The tool is 99% accurate on our test set of radiology reports.

### Limitations
- The tool was not designed initially to redact clinic letters as it was developed primarily on radiology reports.

- It's known significant weaknesses are that it misses postcodes as these were not in its development set.

- It may overly aggressively redact text because it was built as a research tool where precision is prized > recall.

### Demo Test Text
- Redaction Challenge v1. Here is some very tricky to redact pseudo-clinical text. The tool has been validated against this:

1. Dr. Huntington diagnosed Ms. Alzheimer with Alzheimer's disease during her last visit to the Huntington Medical Center. The prognosis was grim, but Dr. Huntington assured Ms. Alzheimer that the facility was well-equipped to handle her condition, despite the lack of a cure for Alzheimer's.

2. Paget Brewster, a 45-year-old woman, was recently diagnosed with Paget's disease of bone by her physician, Dr. Graves. Paget's disease is a chronic disorder that affects bone remodeling, leading to weakened and deformed bones. Brewster's case is not related to Grave's disease, an autoimmune disorder affecting the thyroid gland.

3. Crohn Marshall, a 28-year-old man, has been battling Crohn's disease for the past five years. Crohn's disease is a type of inflammatory bowel disease (IBD) that causes inflammation of the digestive tract. Marshall's condition is managed by his gastroenterologist, Dr. Ulcerative Colitis, who specializes in treating IBD patients.

4. Addison Montgomery, a 32-year-old woman, was rushed to the hospital after experiencing severe abdominal pain and fatigue. After a series of tests, Dr. Cushing diagnosed Montgomery with Addison's disease, a rare disorder of the adrenal glands. Montgomery's condition is not related to Cushing's syndrome, which is caused by excessive cortisol production.

5. Lou Gehrig, a renowned baseball player, was diagnosed with amyotrophic lateral sclerosis (ALS) in 1939. ALS, also known as Lou Gehrig's disease, is a progressive neurodegenerative disorder that affects nerve cells in the brain and spinal cord. Gehrig's diagnosis was confirmed by his neurologist, Dr. Bell, who noted that the condition was not related to Bell's palsy, a temporary facial paralysis.

6. Parkinson Brown, a 62-year-old man, has been living with Parkinson's disease for the past decade. Parkinson's disease is a neurodegenerative disorder that affects movement and balance. Brown's condition is managed by his neurologist, Dr. Lewy Body, who noted that Brown's symptoms were not related to Lewy body dementia, another neurodegenerative disorder.

7. Kaposi Sarcoma, a 35-year-old man, was recently diagnosed with Kaposi's sarcoma, a type of cancer that develops from the cells that line lymph or blood vessels. Sarcoma's diagnosis was confirmed by his oncologist, Dr. Burkitt Lymphoma, who noted that the condition was not related to Burkitt's lymphoma, an aggressive form of non-Hodgkin's lymphoma.

8. Dr. Kawasaki treated young Henoch Schonlein for Henoch-Schönlein purpura, a rare disorder that causes inflammation of the blood vessels. Schonlein's case was not related to Kawasaki disease, a condition that primarily affects children and causes inflammation in the walls of medium-sized arteries.

9. Wilson Menkes, a 42-year-old man, was diagnosed with Wilson's disease, a rare genetic disorder that causes copper to accumulate in the body. Menkes' diagnosis was confirmed by his geneticist, Dr. Niemann Pick, who noted that the condition was not related to Niemann-Pick disease, another rare genetic disorder that affects lipid storage.

10. Dr. Marfan treated Ms. Ehlers Danlos for Ehlers-Danlos syndrome, a group of inherited disorders that affect the connective tissues. Danlos' case was not related to Marfan syndrome, another genetic disorder that affects connective tissue development and leads to abnormalities in the bones, eyes, and cardiovascular system.
"""

default_text = "<Place your Text to Redact Here>"

description = """
*Release Date:* 29/06/2024

*Version:* **1.0** - Working Proof of Concept Demo with API option

*Authors:* **Cai Davis, Michael George, Matt Stammers**
"""

iface = gr.Interface(
    fn=redact,
    inputs=gr.Textbox(placeholder=default_text, label="Input Text", lines=25),
    outputs=gr.Textbox(label="Anonymised Text", lines=25),
    title="SETT: Data and AI. Pteredactyl Demo",
    description=description,
    article=hint,
)

iface.launch(server_name="0.0.0.0", server_port=7800)
