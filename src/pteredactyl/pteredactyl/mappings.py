BASE_CONFIGURATION = {
    "PRESIDIO_SUPPORTED_ENTITIES": [
        "LOCATION",
        "PERSON",
        "ORGANIZATION",
        "AGE",
        "PHONE_NUMBER",
        "EMAIL_ADDRESS",
        "DATE_TIME",
        "DEVICE",
        "ZIP",
        "PROFESSION",
        "USERNAME",
        "ID",
    ],
    "LABELS_TO_IGNORE": ["O"],
    "SUB_WORD_AGGREGATION": "simple",
    "DATASET_TO_PRESIDIO_MAPPING": {
        "DATE": "DATE_TIME",
        "DOCTOR": "PERSON",
        "PATIENT": "PERSON",
        "HOSPITAL": "LOCATION",
        "MEDICALRECORD": "ID",
        "IDNUM": "ID",
        "ORGANIZATION": "ORGANIZATION",
        "ZIP": "ZIP",
        "PHONE": "PHONE_NUMBER",
        "USERNAME": "USERNAME",
        "STREET": "LOCATION",
        "PROFESSION": "PROFESSION",
        "COUNTRY": "LOCATION",
        "LOCATION-OTHER": "LOCATION",
        "FAX": "PHONE_NUMBER",
        "EMAIL": "EMAIL_ADDRESS",
        "STATE": "LOCATION",
        "DEVICE": "DEVICE",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
        "ID": "ID",
    },
    "MODEL_TO_PRESIDIO_MAPPING": {
        "PER": "PERSON",
        "PERSON": "PERSON",
        "LOC": "LOCATION",
        "ORG": "ORGANIZATION",
        "AGE": "AGE",
        "PATIENT": "PERSON",
        "HCW": "PERSON",
        "HOSPITAL": "LOCATION",
        "PATORG": "ORGANIZATION",
        "DATE": "DATE_TIME",
        "PHONE": "PHONE_NUMBER",
        "VENDOR": "ORGANIZATION",
        "ID": "ID",
        "FAC": "ZIP",
        "EMAIL": "EMAIL_ADDRESS",
    },
    "CHUNK_OVERLAP_SIZE": 40,
    "CHUNK_SIZE": 600,
    "ID_SCORE_MULTIPLIER": 0.4,
    "ID_ENTITY_NAME": "ID",
}


def create_configuration(default_model_path, explanation):
    config = BASE_CONFIGURATION.copy()
    config["DEFAULT_MODEL_PATH"] = default_model_path
    config["DEFAULT_EXPLANATION"] = explanation
    return config


configuration = {
    "StanfordAIMI/stanford-deidentifier-base": create_configuration(
        "StanfordAIMI/stanford-deidentifier-base",
        "Identified as {} by the StanfordAIMI/stanford-deidentifier-base NER model",
    ),
    "StanfordAIMI/stanford-deidentifier-with-radiology-reports-and-i2b2": create_configuration(
        "StanfordAIMI/stanford-deidentifier-with-radiology-reports-and-i2b2",
        "Identified as {} by the StanfordAIMI/stanford-deidentifier-with-radiology-reports-and-i2b2 NER model",
    ),
    "lakshyakh93/deberta_finetuned_pii": create_configuration(
        "lakshyakh93/deberta_finetuned_pii",
        "Identified as {} by the lakshyakh93/deberta_finetuned_pii NER model",
    ),
    "urchade/gliner_multi_pii-v1": create_configuration(
        "urchade/gliner_multi_pii-v1",
        "Identified as {} by the urchade/gliner_multi_pii-v1 NER model",
    ),
    "beki/en_spacy_pii_distilbert": create_configuration(
        "beki/en_spacy_pii_distilbert",
        "Identified as {} by the beki/en_spacy_pii_distilbert NER model",
    ),
    "nikhilrk/de-identify": create_configuration(
        "nikhilrk/de-identify", "Identified as {} by the nikhilrk/de-identify NER model"
    ),
}
