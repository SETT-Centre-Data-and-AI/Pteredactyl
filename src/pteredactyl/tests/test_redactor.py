import pandas as pd
import pytest

import pteredactyl as pt


@pytest.fixture
def load_analyser(scope="module"):
    analyzer = pt.create_analyser()


@pytest.fixture
def dummy_text():
    text = "My name is Frank Pus and I live Southampton"
    return text


@pytest.fixture
def expected_redact(dummy_text):
    placeholders = {"<PERSON>": ["Frank Pus"], "<LOCATION>": ["Southampton"]}

    for entity, repl_list in placeholders.items():
        for item in repl_list:
            dummy_text = dummy_text.replace(item, entity)

    return dummy_text


@pytest.fixture
def expected_replacement(dummy_text, replacement_lists):
    replacements = {"Frank Pus": "Alice Smith", "Southampton": "Los Angeles"}

    for entity, repl_item in replacements.items():
        dummy_text = dummy_text.replace(entity, repl_item)

    return dummy_text


@pytest.fixture()
def replacement_lists():
    repl_list = {"PERSON": ["Alice Smith"], "LOCATION": ["Los Angeles"]}
    return repl_list


def test_should_anonymise_text_with_placeholders(
    load_analyser, dummy_text, expected_redact
):
    redacted = pt.anonymise(dummy_text)
    assert redacted == expected_redact


def test_should_anonymise_text_with_custom_entities(
    load_analyser, dummy_text, expected_redact
):
    redacted = pt.anonymise(dummy_text, entities=["PERSON"])
    assert redacted == "My name is <PERSON> and I live Southampton"


def test_should_anonymise_text_with_mask_individual_words(
    load_analyser, dummy_text, expected_redact
):
    redacted = pt.anonymise(dummy_text, entities=["PERSON"], mask_individual_words=True)
    print(redacted)
    assert redacted == "My name is <PERSON> <PERSON> and I live Southampton"


def test_should_anonymise_df(load_analyser, dummy_text, expected_redact):
    COL_TO_REDACT = "text"
    df = pd.DataFrame({COL_TO_REDACT: [dummy_text]})

    redacted_df = pt.anonymise_df(
        df=df,
        column=COL_TO_REDACT,
        inplace=True,
        col_inplace=False,
        highlight=False,
    )

    print(redacted_df)

    assert redacted_df[f"{COL_TO_REDACT}_redacted"].iloc[0] == expected_redact


def test_should_anonymise_with_hide_in_plain_sight(
    load_analyser, dummy_text, expected_replacement, replacement_lists
):
    redacted = pt.anonymise(dummy_text, replacement_lists=replacement_lists)

    assert redacted == expected_replacement


def test_should_anonymise_with_regex_matches(load_analyser):

    text = "RE Mr. Smith, 1 Fake Street, SN1 4AX, 2345678909. Email address: test@example.com"
    expected_replacement = "RE <PERSON>, <LOCATION>, <POSTCODE>, <NHS_NUMBER>. Email address: <EMAIL_ADDRESS>"

    redacted = pt.anonymise(text)
    assert redacted == expected_replacement

    print(redacted)


if __name__ == "__main__":
    pytest.main([__file__])
