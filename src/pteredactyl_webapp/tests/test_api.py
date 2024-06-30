import re

import pytest
import requests
from gradio_client import Client

# Sample texts for testing
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


def extract_tokens(text):
    # Extract tokens like [PERSON], [ID], [LOCATION], etc.
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
            if reference_count[token] > redacted_count[token]:
                fn += reference_count[token] - redacted_count[token]
            elif redacted_count[token] > reference_count[token]:
                fp += redacted_count[token] - reference_count[token]
        else:
            fn += reference_count[token]

    for token in redacted_count:
        if token not in reference_count:
            fp += redacted_count[token]

    return tp, fn, fp


def calculate_true_negatives(total_tokens, total_entities, tp, fn, fp):
    tn = total_tokens - (total_entities + fp + fn + tp)
    return tn


def calculate_metrics(reference_text, redacted_text):
    reference_tokens = extract_tokens(reference_text)
    redacted_tokens = extract_tokens(redacted_text)

    print("Reference Tokens:", reference_tokens)
    print("Redacted Tokens:", redacted_tokens)

    tp, fn, fp = compare_tokens(reference_tokens, redacted_tokens)

    total_tokens = len(reference_text.split())
    total_entities = len(reference_tokens)
    tn = calculate_true_negatives(total_tokens, total_entities, tp, fn, fp)

    return tp, fn, fp, tn


@pytest.fixture
def sample_data():
    redacted_text = """
    1. [PERSON] (Patient No: [ID]) diagnosed [PERSON] with Alzheimer's disease during her last visit to the [LOCATION] on [DATE_TIME]. The prognosis was grim, but [PERSON] assured [PERSON] that the facility was well-equipped to handle her condition despite the lack of a cure for Alzheimer's.

    2. [PERSON] (Patient No: [ID]), a 45-year-old woman, was recently diagnosed with Paget's disease of bone by her physician, [PERSON] at [LOCATION] on [DATE_TIME] Postcode: [POSTCODE]. Paget's disease is a chronic disorder that affects bone remodeling, leading to weakened and deformed bones. [PERSON]'s case is not related to Grave's disease, an autoimmune disorder affecting the thyroid gland.

    3. [PERSON] ([LOCATION] No: [ID]), a 28-year-old man, has been battling Crohn's disease for the past five years. Crohn's disease is a type of inflammatory bowel disease (IBD) that causes inflammation of the digestive tract. [PERSON]'s condition is managed by his gastroenterologist, [PERSON] Ulcerative Colitis, who specializes in treating IBD patients at the [LOCATION].

    4. [PERSON] ([LOCATION] No: [ID]), a 32-year-old woman, was rushed to [LOCATION] on [DATE_TIME] after experiencing severe abdominal pain and fatigue. After a series of tests, [PERSON] diagnosed [PERSON] with Addison's disease, a rare disorder of the adrenal glands. Postcode is [POSTCODE]. [PERSON]'s condition is not related to Cushing's syndrome, which is caused by excessive cortisol production.

    5. [PERSON] ([LOCATION] No: [ID]), a renowned baseball player, was diagnosed with amyotrophic lateral scl[PERSON] (ALS) in 1939 at the [LOCATION]. ALS, also known as Lou Gehrig's disease, is a progressive neurodegenerative disorder that affects nerve cells in the brain and spinal cord. Gehrig's diagnosis was confirmed by his neurologist, [PERSON], who noted that the condition was not related to Bell's palsy, a temporary facial paralysis.

    6. [PERSON] (Patient No No: [ID]), a 62-year-old man, has been living with Parkinson's disease for the past decade. Parkinson's disease is a neurodegenerative disorder that affects movement and balance. [PERSON]'s condition is managed by his neurologist, [PERSON], who noted that Brown's symptoms were not related to Lewy body dementia, another neurodegenerative disorder, at [LOCATION].

    7. Kaposi Sarcoma (Patient No: [ID]), a 35-year-old man, was recently diagnosed with Kaposi's sarcoma, a type of cancer that develops from the cells that line lymph or blood vessels, at [LOCATION] on [DATE_TIME]. Sarcoma's diagnosis was confirmed by his oncologist, [PERSON] Lymphoma, who noted that the condition was not related to Burkitt's lymphoma, an aggressive form of non-Hodgkin's lymphoma. He died on [DATE_TIME].

    8. [PERSON] (Patient No No: [ID]) treated young Henoch Sch[PERSON]lein for Henoch-Schönlein purpura, a rare disorder that causes inflammation of the blood vessels, at [LOCATION] on [DATE_TIME]. [PERSON]'s case was not related to Kawasaki disease, a condition that primarily affects children and causes inflammation in the walls of medium-sized arteries.

    9. [PERSON] ([LOCATION] No: [ID]), a 42-year-old man, was diagnosed with Wilson's disease, a rare genetic di[PERSON] that causes copper to accumulate in the body. [PERSON]' diagnosis was confirmed by his geneticist, [PERSON], at [LOCATION] on [DATE_TIME], who noted that the condition was not related to Niemann-Pick disease, another rare genetic disorder that affects lipid storage. Postcode was [POSTCODE].

    10. [PERSON] (Patient No No: [ID]) treated [PERSON] for Ehlers-Danlos syndrome, a group of inherited disorders that affect the connective tissues, at the [LOCATION] on [DATE_TIME]. [PERSON]' case was not related to Marfan syndrome, another genetic disorder that affects connective tissue development and leads to abnormalities in the bones, eyes, and cardiovascular system. [PERSON]'s username is: [PERSON]
    """
    return reference_text, redacted_text


@pytest.fixture
def client():
    return Client("http://localhost:7860/")


def test_server_running():
    try:
        response = requests.get("http://localhost:7860")
        response.raise_for_status()
    except requests.exceptions.HTTPError as errH:
        pytest.fail(f"HTTP Error: {errH}")
    except requests.exceptions.ConnectionError as errC:
        pytest.fail(f"Error Connecting: {errC}")
    except requests.exceptions.Timeout as errT:
        pytest.fail(f"Timeout Error: {errT}")
    except requests.exceptions.RequestException as err:
        pytest.fail(f"Request Exception: {err}")


def test_api_redaction(client, sample_data):
    reference_text, expected_redacted_text = sample_data
    result = client.predict(text=reference_text, api_name="/predict")

    redacted_text_result = result[
        0
    ]  # Assuming the first element in the tuple is the redacted text

    tp, fn, fp, tn = calculate_metrics(reference_text, redacted_text_result)

    assert tp > 0, "True positives should be greater than zero"
    assert fn >= 0, "False negatives should be non-negative"
    assert fp >= 0, "False positives should be non-negative"
    assert tn >= 0, "True negatives should be non-negative"

    print(f"True Positives: {tp}")
    print(f"False Negatives: {fn}")
    print(f"False Positives: {fp}")
    print(f"True Negatives: {tn}")


if __name__ == "__main__":
    pytest.main()
