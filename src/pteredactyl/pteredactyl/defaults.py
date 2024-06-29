from pteredactyl.regex_entities import REGEX_ENTITIES

DEFAULT_SPACY_MODEL = "en_core_web_sm"
DEFAULT_NER_MODEL = "StanfordAIMI/stanford-deidentifier-base"

DEFAULT_ENTITIES = [
    "LOCATION",
    "PERSON",
    "ORGANIZATION",
    "AGE",
    "PHONE_NUMBER",
    "DATE_TIME",
    "DEVICE",
    "ZIP",
    "PROFESSION",
    "USERNAME",
    "ID",
]

SPACY_LABELS_TO_IGNORE = {
    "O",
    "ORG",
    "ORGANIZATION",
    "CARDINAL",
    "EVENT",
    "LANGUAGE",
    "LAW",
    "MONEY",
    "ORDINAL",
    "PERCENT",
    "PRODUCT",
    "QUANTITY",
    "WORK_OF_ART",
    "FAC",
}

DEFAULT_REGEX_ENTITIES = [entity_type for entity_type in REGEX_ENTITIES.keys()]


def show_defaults() -> None:
    """
    Print the default values used by pteredactyl.

    This function shows the default values for the following variables:
    - DEFAULT_NER_MODEL (for model_path)
    - DEFAULT_SPACY_MODEL (for spacy_model)
    - DEFAULT_ENTITIES (for entities)
    - DEFAULT_REGEX_ENTITIES (for regex_entities)

    Returns
    -------
    None
    """
    print("PteRedactyl Defaults")
    print("--------------------")
    print(f"DEFAULT_NER_MODEL:      {DEFAULT_NER_MODEL}")
    print(f"DEFAULT_SPACY_MODEL:    {DEFAULT_SPACY_MODEL}")
    print(f"DEFAULT_ENTITIES:       {DEFAULT_ENTITIES}")
    print(f"DEFAULT_REGEX_ENTITIES: {DEFAULT_REGEX_ENTITIES}")


def change_model(new_model: str) -> None:
    """
    Change the default NER model.

    Parameters
    ----------
    new_model : str
        The new model path to be set as the default NER model.

    Returns
    -------
    None
    """
    global DEFAULT_NER_MODEL
    DEFAULT_NER_MODEL = new_model
    print(f"DEFAULT_NER_MODEL changed to: {DEFAULT_NER_MODEL}")
