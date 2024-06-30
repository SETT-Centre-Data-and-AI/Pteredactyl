import logging
import logging.config
import re
from pathlib import Path

import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml

import pteredactyl as pt
from pteredactyl.defaults import change_model

# Logging configuration. This is only done at root level
logging_config = yaml.safe_load(Path("logging.yaml").read_text())
logging.config.dictConfig(logging_config)

# Get the logger
log = logging.getLogger(__name__)

# Load the model
log.info("Starting App")

sample_text = """
1. Dr. Huntington (Patient No: 1234567890) diagnosed Ms. Alzheimer with Alzheimer's disease during her last visit to the Huntington Medical Center on 12/12/2023. The prognosis was grim, but Dr. Huntington assured Ms. Alzheimer that the facility was well-equipped to handle her condition despite the lack of a cure for Alzheimer's.

2. Paget Brewster (Patient No: 0987654321), a 45-year-old woman, was recently diagnosed with Paget's disease of bone by her physician, Dr. Graves at St. Jenny's Hospital on 01/06/2026 Postcode: JE30 6YN. Paget's disease is a chronic di[PERSON]der that affects bone remodeling, leading to weakened and deformed bones. Brewster's case is not related to Grave's disease, an autoimmune disorder affecting the thyroid gland.

3. Crohn Marshall (Patient No: 943 476 5918), a 28-year-old man, has been battling Crohn's disease for the past five years. Crohn's disease is a type of inflammatory bowel disease (IBD) that causes inflammation of the digestive tract. Marshall's condition is managed by his gastroenterologist, Dr. Ulcerative Colitis, who specializes in treating IBD patients at the Royal Free Hospital.

4. Addison Montgomery (NHS No: 5566778899), a 32-year-old woman, was rushed to University College Hospital on 18/09/2023 after experiencing severe abdominal pain and fatigue. After a series of tests, Dr. Cushing diagnosed Montgomery with Addison's disease, a rare disorder of the adrenal glands. Postcode is NH77 9AF. Montgomery's condition is not related to Cushing's syndrome, which is caused by excessive cortisol production.

5. Lou Gehrig (NHS No: 943 476 5919), a renowned baseball player, was diagnosed with amyotrophic lateral sclerosis (ALS) in 1939 at the Mayo Clinic. ALS, also known as Lou Gehrig's disease, is a progressive neurodegenerative disorder that affects nerve cells in the brain and spinal cord. Gehrig's diagnosis was confirmed by his neurologist, Dr. Bell, who noted that the condition was not related to Bell's palsy, a temporary facial paralysis.

6. Parkinson Brown (Patient No No: 3344556677), a 62-year-old man, has been living with Parkinson's disease for the past decade. Parkinson's disease is a neurodegenerative disorder that affects movement and balance. Brown's condition is managed by his neurologist, Dr. Lewy Body, who noted that Brown's symptoms were not related to Lewy body dementia, another neurodegenerative disorder, at King's College Hospital.

7. Kaposi Sarcoma (Patient No: 9988776655), a 35-year-old man, was recently diagnosed with Kaposi's sarcoma, a type of cancer that develops from the cells that line lymph or blood vessels, at Guy's Hospital on 17/04/2023. Sarcoma's diagnosis was confirmed by his oncologist, Dr. Burkitt Lymphoma, who noted that the condition was not related to Burkitt's lymphoma, an aggressive form of non-Hodgkin's lymphoma. He died on 17/04/2023.

8. Dr. Kawasaki (Patient No No: 2233445566) treated young Henoch Schonlein for Henoch-Schönlein purpura, a rare disorder that causes inflammation of the blood vessels, at Great Ormond Street Hospital on 05/05/2024. Schonlein's case was not related to Kawasaki disease, a condition that primarily affects children and causes inflammation in the walls of medium-sized arteries.

9. Wilson Menkes (NHS No: 943 476 5916), a 42-year-old man, was diagnosed with Wilson's disease, a rare genetic disorder that causes copper to accumulate in the body. Menkes' diagnosis was confirmed by his geneticist, Dr. Niemann Pick, at Addenbrooke's Hospital on 02/02/2025, who noted that the condition was not related to Niemann-Pick disease, another rare genetic disorder that affects lipid storage. Postcode was GH75 3HF.

10. Dr. Marfan (Patient No No: 4455667788) treated Ms. Ehlers Danlos for Ehlers-Danlos syndrome, a group of inherited disorders that affect the connective tissues, at the Royal Brompton Hospital on 30/11/2024. Danlos' case was not related to Marfan syndrome, another genetic disorder that affects connective tissue development and leads to abnormalities in the bones, eyes, and cardiovascular system. Dr Jab's username is: jabba
"""

# Gold Standard Text
reference_text = """
1. [PERSON] (Patient No: [ID]) diagnosed [PERSON] with Alzheimer's disease during her last visit to the [LOCATION] on [DATE_TIME]. The prognosis was grim, but [PERSON] assured [PERSON] that the facility was well-equipped to handle her condition despite the lack of a cure for Alzheimer's.

2. [PERSON] (Patient No: [ID]), a 45-year-old woman, was recently diagnosed with Paget's disease of bone by her physician, [PERSON] at [LOCATION] on [DATE_TIME] Postcode: [POSTCODE]. Paget's disease is a chronic disorder that affects bone remodeling, leading to weakened and deformed bones. [PERSON]'s case is not related to Grave's disease, an autoimmune disorder affecting the thyroid gland.

3. [PERSON] ([LOCATION] No: [NHS_NUMBER]), a 28-year-old man, has been battling Crohn's disease for the past five years. Crohn's disease is a type of inflammatory bowel disease (IBD) that causes inflammation of the digestive tract. [PERSON]'s condition is managed by his gastroenterologist, [PERSON] Ulcerative Colitis, who specializes in treating IBD patients at the [LOCATION].

4. [PERSON] (Patient No: [ID]), a 32-year-old woman, was rushed to [LOCATION] on [DATE_TIME] after experiencing severe abdominal pain and fatigue. After a series of tests, [PERSON] diagnosed [PERSON] with Addison's disease, a rare disorder of the adrenal glands. Postcode is [POSTCODE]. [PERSON]'s condition is not related to Cushing's syndrome, which is caused by excessive cortisol production.

5. [PERSON] ([LOCATION] No: [NHS_NUMBER]), a renowned baseball player, was diagnosed with amyotrophic lateral sclerosis (ALS) in 1939 at the [LOCATION]. ALS, also known as Lou Gehrig's disease, is a progressive neurodegenerative disorder that affects nerve cells in the brain and spinal cord. Gehrig's diagnosis was confirmed by his neurologist, [PERSON], who noted that the condition was not related to Bell's palsy, a temporary facial paralysis.

6. [PERSON] (Patient No: [ID]), a 62-year-old man, has been living with Parkinson's disease for the past decade. Parkinson's disease is a neurodegenerative disorder that affects movement and balance. [PERSON]'s condition is managed by his neurologist, [PERSON], who noted that [PERSON]'s symptoms were not related to Lewy body dementia, another neurodegenerative disorder, at [LOCATION].

7. [PERSON] (Patient No: [ID]), a 35-year-old man, was recently diagnosed with Kaposi's sarcoma, a type of cancer that develops from the cells that line lymph or blood vessels, at [LOCATION] on [DATE_TIME]. Sarcoma's diagnosis was confirmed by his oncologist, [PERSON] Lymphoma, who noted that the condition was not related to Burkitt's lymphoma, an aggressive form of non-Hodgkin's lymphoma. He died on [DATE_TIME].

8. [PERSON] (Patient No: [ID]) treated young Henoch Schonlein for Henoch-Schönlein purpura, a rare disorder that causes inflammation of the blood vessels, at [LOCATION] on [DATE_TIME]. [PERSON]'s case was not related to Kawasaki disease, a condition that primarily affects children and causes inflammation in the walls of medium-sized arteries.

9. [PERSON] ([LOCATION] No: [NHS_NUMBER]), a 42-year-old man, was diagnosed with Wilson's disease, a rare genetic disorder that causes copper to accumulate in the body. [PERSON]'s diagnosis was confirmed by his geneticist, [PERSON], at [LOCATION] on [DATE_TIME], who noted that the condition was not related to Niemann-Pick disease, another rare genetic disorder that affects lipid storage. Postcode was [POSTCODE].

10. [PERSON] (Patient No: [ID]) treated [PERSON] for Ehlers-Danlos syndrome, a group of inherited disorders that affect the connective tissues, at the [LOCATION] on [DATE_TIME]. [PERSON]'s case was not related to Marfan syndrome, another genetic disorder that affects connective tissue development and leads to abnormalities in the bones, eyes, and cardiovascular system. Dr [PERSON]'s username is: [USERNAME]
"""


def redact(text: str, model_name: str):
    model_paths = {
        "Stanford Base De-Identifier": "StanfordAIMI/stanford-deidentifier-base",
        # "Stanford with Radiology and i2b2": "StanfordAIMI/stanford-deidentifier-with-radiology-reports-and-i2b2",
        "Deberta PII": "lakshyakh93/deberta_finetuned_pii",
        # "Gliner PII": "urchade/gliner_multi_pii-v1",
        # "Spacy PII": "beki/en_spacy_pii_distilbert",
        "Nikhilrk De-Identify": "nikhilrk/de-identify",
    }

    model_path = model_paths.get(model_name, "StanfordAIMI/stanford-deidentifier-base")

    # Log the model being changed to
    log.info(f"Changing to model: {model_path}")

    if model_path:
        change_model(model_path)
    else:
        raise ValueError("No valid model path provided.")

    anonymized_text = pt.anonymise(text, model_path=model_path)  # Pass model_path
    anonymized_text = anonymized_text.replace("<", "[").replace(">", "]")
    return anonymized_text


def extract_tokens(text):
    tokens = re.findall(r"\[(.*?)\]", text)
    return tokens


def compare_tokens(reference_tokens, redacted_tokens):
    tp = 0
    fn = 0
    fp = 0

    reference_count = {
        token: reference_tokens.count(token) for token in set(reference_tokens)
    }
    redacted_count = {
        token: redacted_tokens.count(token) for token in set(redacted_tokens)
    }

    for token in reference_count:
        if token in redacted_count:
            tp += min(reference_count[token], redacted_count[token])
            fn += max(reference_count[token] - redacted_count[token], 0)
            fp += max(redacted_count[token] - reference_count[token], 0)
        else:
            fn += reference_count[token]

    for token in redacted_count:
        if token not in reference_count:
            fp += redacted_count[token]

    return tp, fn, fp


def calculate_true_negatives(total_tokens, total_entities, tp, fn, fp):
    tn = total_tokens - (total_entities + fp + fn + tp)
    return tn


def count_entities_and_compute_metrics(reference_text: str, redacted_text: str):
    reference_tokens = extract_tokens(reference_text)
    redacted_tokens = extract_tokens(redacted_text)

    tp_count, fn_count, fp_count = compare_tokens(reference_tokens, redacted_tokens)

    total_tokens = len(reference_text.split())
    total_entities = len(reference_tokens)
    tn_count = calculate_true_negatives(
        total_tokens, total_entities, tp_count, fn_count, fp_count
    )

    return tp_count, fn_count, fp_count, tn_count


def flag_errors(reference_text: str, redacted_text: str):
    fn_count = 0
    fp_count = 0

    reference_tokens = [
        (match.group(1), match.start())
        for match in re.finditer(r"\[(.*?)\]", reference_text)
    ]
    redacted_tokens = [
        (match.group(1), match.start())
        for match in re.finditer(r"\[(.*?)\]", redacted_text)
    ]

    reference_set = set(token for token, _ in reference_tokens)
    redacted_set = set(token for token, _ in redacted_tokens)

    flagged_reference_text = reference_text
    flagged_redacted_text = redacted_text

    for token, _ in reference_tokens:
        if token not in redacted_set:
            fn_count += 1
            flagged_reference_text = flagged_reference_text.replace(
                f"[{token}]", f"[FALSE_NEGATIVE]{token}[/FALSE_NEGATIVE]"
            )

    for token, _ in redacted_tokens:
        if token not in reference_set and token not in [
            "FALSE_NEGATIVE",
            "/FALSE_NEGATIVE",
        ]:
            fp_count += 1
            flagged_redacted_text = flagged_redacted_text.replace(
                f"[{token}]", f"[FALSE_POSITIVE]{token}[/FALSE_POSITIVE]"
            )

    return flagged_reference_text, flagged_redacted_text, fn_count, fp_count


def visualize_entities(redacted_text: str):
    colors = {
        "PERSON": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "ID": "linear-gradient(90deg, #ff9a9e, #fecfef)",
        "GPE": "linear-gradient(90deg, #fccb90, #d57eeb)",
        "NHS_NUMBER": "linear-gradient(90deg, #ff9a9e, #fecfef)",
        "DATE_TIME": "linear-gradient(90deg, #fddb92, #d1fdff)",
        "LOCATION": "linear-gradient(90deg, #a1c4fd, #c2e9fb)",
        "EVENT": "linear-gradient(90deg, #a6c0fe, #f68084)",
        "POSTCODE": "linear-gradient(90deg, #c2e59c, #64b3f4)",
        "USERNAME": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "FALSE_NEGATIVE": "linear-gradient(90deg, #ff6b6b, #ff9a9e)",  # Red for false negatives
        "/FALSE_NEGATIVE": "linear-gradient(90deg, #ff6b6b, #ff9a9e)",  # Red for false negatives
        "FALSE_POSITIVE": "linear-gradient(90deg, #ffcccb, #ff6666)",  # Light red for false positives
        "/FALSE_POSITIVE": "linear-gradient(90deg, #ffcccb, #ff6666)",  # Light red for false positives
    }

    token_colors = {
        "[PERSON]": "PERSON",
        "[LOCATION]": "LOCATION",
        "[ID]": "ID",
        "[NHS_NUMBER]": "NHS_NUMBER",
        "[DATE_TIME]": "DATE_TIME",
        "[EVENT]": "EVENT",
        "[POSTCODE]": "POSTCODE",
        "[USERNAME]": "USERNAME",
        "[FALSE_NEGATIVE]": "FALSE_NEGATIVE",
        "[/FALSE_NEGATIVE]": "/FALSE_NEGATIVE",
        "[FALSE_POSITIVE]": "FALSE_POSITIVE",
        "[/FALSE_POSITIVE]": "/FALSE_POSITIVE",
    }

    def wrap_token_in_html(text, token, color):
        parts = text.split(token)
        wrapped_token = f'<span style="background: {color}; padding: 2px; border-radius: 3px;">{token}</span>'
        return wrapped_token.join(parts)

    for token, color_class in token_colors.items():
        redacted_text = wrap_token_in_html(redacted_text, token, colors[color_class])

    return f'<div style="white-space: pre-wrap; border: 1px solid #ccc; padding: 10px; border-radius: 5px;">{redacted_text}</div>'


def generate_confusion_matrix(tp_count, fn_count, fp_count, tn_count):
    data = {
        "Actual Positive": [tp_count, fn_count],
        "Actual Negative": [fp_count, tn_count],
    }
    df = pd.DataFrame(data, index=["Predicted Positive", "Predicted Negative"])
    plt.figure(figsize=(8, 6))
    sns.heatmap(df, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    return plt


def calculate_metrics(tp_count, fn_count, fp_count, tn_count):
    accuracy = (tp_count + tn_count) / (tp_count + fn_count + fp_count + tn_count)
    precision = tp_count / (tp_count + fp_count) if (tp_count + fp_count) > 0 else 0
    recall = tp_count / (tp_count + fn_count) if (tp_count + fn_count) > 0 else 0
    f1_score = (
        2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    )
    metrics_table = f"""
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Accuracy: [(TP+TN) / (TP + FN + FP + TN)] </td><td>{accuracy:.2f}</td></tr>
        <tr><td>Precision: [TP / (TP + FP)] </td><td>{precision:.2f}</td></tr>
        <tr><td>Recall: [TP / (TP + FN)] </td><td>{recall:.2f}</td></tr>
        <tr><td>F1 Score: [2 * Precision * Recall / (Precision + Recall)] </td><td>{f1_score:.2f}</td></tr>
    </table>
    """
    return metrics_table


def redact_and_visualize(text: str, model_name: str):
    total_tokens = len(reference_text.split())

    # Redact the text
    redacted_text = redact(text, model_name)

    # Flag false positives and false negatives
    reference_text_with_fn, redacted_text_with_fp, fn_count, fp_count = flag_errors(
        reference_text, redacted_text
    )

    # Print the final texts with flags for debugging
    log.debug("Final Reference Text with False Negatives:")
    log.debug(reference_text_with_fn)
    log.debug("\nFinal Redacted Text with False Positives:")
    log.debug(redacted_text_with_fp)

    # Count entities and compute metrics
    tp_count, fn_count, fp_count, tn_count = count_entities_and_compute_metrics(
        reference_text_with_fn, redacted_text_with_fp
    )

    # Visualize the redacted text
    visualized_html = visualize_entities(redacted_text_with_fp)

    # Generate confusion matrix and metrics table
    confusion_matrix_plot = generate_confusion_matrix(
        tp_count, fn_count, fp_count, tn_count
    )
    metrics_table = calculate_metrics(tp_count, fn_count, fp_count, tn_count)

    return (
        visualized_html,
        f"Total False Negatives: {fn_count}",
        f"Total True Positives: {tp_count}",
        f"Total True Negatives: {tn_count}",
        f"Total False Positives: {fp_count}",
        confusion_matrix_plot,
        metrics_table,
    )


hint = """
## Pteredactyl Gradio Webapp and API

Clinical patient identifiable information (cPII) presents a significant challenge in natural language processing (NLP) that has yet to be fully resolved but significant progress is being made [1,2].

This is why we created [Pteredactyl](https://pypi.org/project/pteredactyl/) - a python module to help with redaction of clinical free text.

## Tool Usage Instructions

When the input text is entered, the tool redacts the cPII from the entered text using NLP with labelled masking tokens and then assesses the models results. You can test the text against different models by selecting from the dropdown.

## Deployment Options

This webapp is available online as a gradio app on Huggingface: [Huggingface Gradio App](https://huggingface.co/spaces/MattStammers/pteredactyl_PII). It is also available as [source](https://github.com/SETT-Centre-Data-and-AI/PteRedactyl) or as a Docker Image: [Docker Image](https://registry.hub.docker.com/r/mattstammers/pteredactyl). All are MIT licensed.

Please note if deploying the docker image the port bindings are to 7860. The image can also be deployed from source using the following command:

```bat
docker build -t pteredactyl:latest .
docker run -d -p 7860:7860 --name pteredactyl-app pteredactyl:latest
```

## Information

A lot of work and experimentation has gone into the development of this tool. Because we believe in being fully transparent further details are given below.


### Methods:

We evaluated three open-source models from Huggingface: Stanford Base De-Identifier, Deberta PII, and Nikhilrk De-Identify using our Clinical_PII_Redaction_Test dataset. The text was tokenised, and all entities such as [PERSON], [ID], and [LOCATION] were tagged in the gold standard. Each model redacted cPII from clinical texts, and outputs were compared to the gold standard template to calculate the confusion matrix, accuracy, precision, recall, and F1 score.

### Results

The full results of the tool are given below in <i>Table 1</i> below.

| Metric     | Stanford Base De-Identifier | Deberta PII | Nikhilrk De-Identify |
|------------|-----------------------------|-------------|----------------------|
| Accuracy   | 0.98                        | 0.85        | 0.68                 |
| Precision  | 0.91                        | 0.93        | 0.28                 |
| Recall     | 0.94                        | 0.16        | 0.49                 |
| F1 Score   | 0.93                        | 0.28        | 0.36                 |
<small><i>Table 1: Summary of Model Performance Metrics</i></small>

### Strengths
- The test benchmark [Clinical_PII_Redaction_Test](https://huggingface.co/datasets/MattStammers/Clinical_PII_Redaction_Test) intentionally exploits commonly observed weaknesses in NLP cPII token masking systems such as clinician/patient/diagnosis name similarity and commonly observed ID/username and location/postcode issues.

- [The Stanford De-Identifier Base Model](https://huggingface.co/StanfordAIMI/stanford-deidentifier-base)[1] is 99% accurate on our test set of radiology reports and achieves an F1 score of 93% on our challenging open-source benchmark. The others models are really to demonstrate the potential of Pteredactyl to deploy any transfomer model.

- We have submitted the code to [OHDSI](https://www.ohdsi.org/) as an abstract and aim strongly to incorporate this into a wider open-source effort to solve intractable clinical informatics problems.

### Limitations
- The tool was not designed initially to redact clinic letters as it was developed primarily on radiology reports in the US. We have made some augmentations to cover elements like postcodes using checksums but these might not always work. The same is true of NHS numbers as illustrated above.

- It may overly aggressively redact text because it was built as a research tool where precision is prized > recall. However, in our experience this is uncommon enough that it is still very useful.

- This is very much a research tool and should not be relied upon as a catch-all in any production-type capacity. The app makes the limitations very transparently obvious via the attached confusion matrix.

### Conclusion
The validation cohort introduced in this study proves to be a highly effective tool for discriminating the performance of open-source cPII redaction models. Intentionally exploiting common weaknesses in cNLP token masking systems offers a more rigorous cPII benchmark than many larger datasets provide.

We invite the open-source community to collaborate to improve the present results and enhance the robustness of cPII redaction methods by building on the work we have begun here [here](https://github.com/SETT-Centre-Data-and-AI/PteRedactyl).

### References:
1. Chambon PJ, Wu C, Steinkamp JM, Adleberg J, Cook TS, Langlotz CP. Automated deidentification of radiology reports combining transformer and “hide in plain sight” rule-based methods. J Am Med Inform Assoc. 2023 Feb 1;30(2):318–28.
2. Kotevski DP, Smee RI, Field M, Nemes YN, Broadley K, Vajdic CM. Evaluation of an automated Presidio anonymisation model for unstructured radiation oncology electronic medical records in an Australian setting. Int J Med Inf. 2022 Dec 1;168:104880.
"""

description = """
*Release Date:* 29/06/2024

*Version:* **1.0** - Working Proof of Concept Demo with API option and webapp demonstration.

*Authors:* **Matt Stammers🧪, Cai Davis🥼 and Michael George🩺**
"""

iface = gr.Interface(
    fn=redact_and_visualize,
    inputs=[
        gr.Textbox(value=sample_text, label="Input Text", lines=25),
        gr.Dropdown(
            choices=[
                "Stanford Base De-Identifier",
                # "Stanford with Radiology and i2b2",
                "Deberta PII",
                # "Gliner PII",
                # "Spacy PII",
                "Nikhilrk De-Identify",
            ],
            label="Model",
            value="Stanford Base De-Identifier",  # Make sure this matches one of the choices
        ),
    ],
    outputs=[
        gr.HTML(label="Anonymised Text with Visualization"),
        gr.Textbox(label="Total False Negatives", lines=1),
        gr.Textbox(label="Total True Positives", lines=1),
        gr.Textbox(label="Total True Negatives", lines=1),
        gr.Textbox(label="Total False Positives", lines=1),
        gr.Plot(label="Confusion Matrix"),
        gr.HTML(label="Evaluation Metrics"),
    ],
    title="SETT: Data and AI. Pteredactyl Demo",
    description=description,
    article=hint,
)

iface.launch()
