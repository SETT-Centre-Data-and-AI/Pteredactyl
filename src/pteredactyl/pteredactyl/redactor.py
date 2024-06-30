import copy
import logging
import random
from collections.abc import Sequence

import pandas as pd
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.recognizer_result import RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import ConflictResolutionStrategy, OperatorConfig
from presidio_anonymizer.operators import OperatorType
from tqdm.auto import tqdm

from pteredactyl.defaults import (
    DEFAULT_ENTITIES,
    DEFAULT_NER_MODEL,
    DEFAULT_REGEX_ENTITIES,
    DEFAULT_SPACY_MODEL,
    change_model,
)
from pteredactyl.recognisers.pteredactyl_recogniser import PteredactylRecogniser
from pteredactyl.regex_entities import (
    build_regex_entity_recogniser_list,
    rebuild_analyser_regex_recognisers,
)
from pteredactyl.support import (
    highlight_text,
    load_nlp_configuration,
    load_nlp_engine,
    load_registry,
    load_spacy_model,
    load_transformers_recognizer,
    return_allowed_results,
    split_results_into_individual_words,
)

presidio_logger = logging.getLogger("presidio-analyzer")


def create_analyser(
    model_path: str = None,
    spacy_model: str = DEFAULT_SPACY_MODEL,
    language: str = "en",
    regex_entities: Sequence[str | PteredactylRecogniser] = DEFAULT_REGEX_ENTITIES,
) -> AnalyzerEngine:
    """
    Create an analyser engine with a Transformers NER model and spaCy model.
    """
    if not model_path:
        raise ValueError("No model path provided for NER model.")

    print(f"Using model path: {model_path}")

    if regex_entities:
        regex_entities = build_regex_entity_recogniser_list(
            regex_entities=regex_entities
        )

    load_spacy_model(spacy_model)

    transformers_recogniser = load_transformers_recognizer(model_path)

    nlp_configuration = load_nlp_configuration(
        language=language, spacy_model=spacy_model
    )

    registry = load_registry(
        transformers_recogniser=transformers_recogniser, regex_entities=regex_entities
    )

    nlp_engine = load_nlp_engine(
        presidio_logger=presidio_logger, nlp_configuration=nlp_configuration
    )

    analyser = AnalyzerEngine(nlp_engine=nlp_engine, registry=registry)

    return analyser


def analyse(
    text: str,
    analyser: AnalyzerEngine | None = None,
    entities: str | list[str] = DEFAULT_ENTITIES,
    regex_entities: Sequence[str | PteredactylRecogniser] = DEFAULT_REGEX_ENTITIES,
    model_path: str = None,
    spacy_model: str = DEFAULT_SPACY_MODEL,
    language: str = "en",
    mask_individual_words: bool = False,
    text_separator: str = " ",
    rebuild_regex_recognisers: bool = True,
    **kwargs,
) -> list[RecognizerResult]:
    """
    Analyses text using the provided NER models and entities, and returns list of those identified.
    It is recommended to first create an analyser and feed this in to be reused with:
        >>> analyser = create_analyser()
        >>> analyser(text=text, analyser=analyser)

    Args:
        text (str): The text to be analyzed.
        analyser (AnalyzerEngine, optional): An instance of AnalyzerEngine. If not provided, a new analyser will be created
            (recommend creating first viacreate_analyser(), before feeding in).
        entities (list, optional): A list of entity types to analyse. If not provided, a default list will be used.
        regex_entities (list, optional): A list of regex entities or PteredactylRecognisers to analyse. If not provided, a default list will be used.
        model_path (str): The path to the model used for analysis (e.g. 'StanfordAIMI/stanford-deidentifier-base'). Used only if analyser not provided.
        spacy_model (str): The spaCy model to use (e.g. 'en_core_web_sm'). Used only if analyser not provided.
        language (str): The language of the text to be analyzed. Defaults to "en". Used only if analyser not provided.
        mask_individual_words (bool): If True, prevents joining of next-door entities together.
            (i.e. with Jane Smith, both 'Jane' and 'Smith' are identified separately if True, combined if False). Defaults to False.
        text_separator (str): Text separator. Default is whitespace.
        rebuild_regex_recognisers (bool): If True, and an existing analyser is provided, the analyser's regex recognisers will be rebuilt before execution.
        **kwargs: Additional keyword arguments for the analyzer.

    Returns:
        list: The analysis results.

    Example:
        >>> from pteredactyl.redactor import analyse
        >>> text = "My name is John Doe and my NHS number is 7890123450"
        >>> results = analyse(text)
        >>> print(results)
        [RecognizerResult(entity_type='PERSON', start=10, end=19, score=1.0),
         RecognizerResult(entity_type='NHS_NUMBER', start=36, end=46, score=1.0)]
    """

    # Prepare
    entities = [entities] if isinstance(entities, str) else entities if entities else []
    regex_entities = (
        build_regex_entity_recogniser_list(regex_entities=regex_entities)
        if regex_entities
        else []
    )
    allowed_entities = entities
    allowed_regex_entities = [
        regex_entity.entity_type for regex_entity in regex_entities
    ]
    entities = allowed_entities + allowed_regex_entities

    # Check Analyser
    if not analyser:
        analyser = create_analyser(
            model_path=model_path,
            spacy_model=spacy_model,
            language=language,
            regex_entities=regex_entities,
        )
    else:
        if rebuild_regex_recognisers:
            rebuild_analyser_regex_recognisers(
                analyser=analyser, regex_entities=regex_entities
            )

    # Analyse
    initial_results = analyser.analyze(
        text, language=language, entities=entities, **kwargs
    )

    if mask_individual_words:
        initial_results = split_results_into_individual_words(
            text=text, results=initial_results, text_separator=text_separator
        )

    results = return_allowed_results(
        initial_results=initial_results,
        allowed_entities=allowed_entities,
        allowed_regex_entities=allowed_regex_entities,
    )

    results.sort(key=lambda x: x.start)

    return results


def anonymise(
    text: str,
    analyser: AnalyzerEngine | None = None,
    entities: str | list[str] = DEFAULT_ENTITIES,
    regex_entities: Sequence[str | PteredactylRecogniser] = DEFAULT_REGEX_ENTITIES,
    highlight: bool = False,
    replacement_lists: dict | None = None,
    model_path: str = None,
    spacy_model: str = DEFAULT_SPACY_MODEL,
    language: str = "en",
    mask_individual_words: bool = False,
    text_separator: str = " ",
    rebuild_regex_recognisers: bool = True,
    **kwargs,
) -> str:
    """
    Anonymises the given text by replacing specified entities by NER, and and regex entities by REGEX. Regex entities take priority and are analysed first.
    It is recommended to first create an analyser and feed this in to be reused.

    Args:
    text (str): The text to be anonymized.
    analyser (AnalyzerEngine, optional): An instance of AnalyzerEngine. If not provided, a new analyser will be created.
    entities (list, optional): A list of entity types to anonymize. If not provided, a default list will be used.
    regex_entities (list, optional): A list of regex entities or PteredactylRecognisers to analyse. If not provided, a default list will be used.
    highlight (bool): If True, highlights the anonymized parts in the text.
    replacement_lists: (dict, optional): A dictionary with entity types as keys and lists of replacement values for hide-in-plain-sight redaction.
    model_path (str): The path to the model used for analysis. Used only if analyser not provided.
    spacy_model (str): The spaCy model to use. Used only if analyser not provided.
    language (str): The language of the text to be analyzed. Defaults to "en". Used only if analyser not provided.
    mask_individual_words (bool): If True, prevents joining of next-door entities together.
            (i.e. Jane Smith becomes <PERSON> <PERSON> if True, or <PERSON> if False). Defaults to False.
    text_separator (str): Text separator. Default is whitespace.
    rebuild_regex_recognisers (bool): If True, and an existing analyser is provided, the analyser's regex recognisers will be rebuilt before execution.
    **kwargs: Additional keyword arguments for analyse.

    Returns:
    str: The anonymized text.

    Example:
        >>> analyser = create_analyser()
        >>> text = '''
            Patient Name: John Doe
            NHS Number: 7890123450
            Address: AB1 0CD
            Date: January 1, 2022
            Diagnostic Findings:
            The CT scan of the patient's chest revealed a mass in the right upper lobe of the lungs.
            The mass is suspected to be malignant and is likely to be a tumor.
            Further diagnostic tests, such as biopsy or CT scan of the mass, may be required to confirm the diagnosis.
            Recommendations:
            The patient is advised to consult with a medical specialist for a thorough evaluation of the mass.
            If the tumor is malignant, further treatment, such as surgery or radiotherapy, may be recommended.
            '''

        >>> results = anonymise(text, analyser=analyser, entities=["DATE_TIME", "PERSON"], regex_recognizers=["POSTCODE", "NHS_NUMBER"])
        >>> print(results)

            Patient Name: <PERSON>
            NHS Number: <NHS_NUMBER>
            Address: <POSTCODE>
            Date: <DATE_TIME>
            Diagnostic Findings:
            The CT scan of the patient's chest revealed a mass in the right upper lobe of the lungs.
            The mass is suspected to be malignant and is likely to be a tumor.
            Further diagnostic tests, such as biopsy or CT scan of the mass, may be required to confirm the diagnosis.
            Recommendations:
            The patient is advised to consult with a medical specialist for a thorough evaluation of the mass.
            If the tumor is malignant, further treatment, such as surgery or radiotherapy, may be recommended.
    """
    # Prepare
    entities = [entities] if isinstance(entities, str) else entities if entities else []
    regex_entities = (
        build_regex_entity_recogniser_list(regex_entities=regex_entities)
        if regex_entities
        else []
    )
    allowed_entities = entities
    allowed_regex_entities = [
        regex_entity.entity_type for regex_entity in regex_entities
    ]
    entities = allowed_entities + allowed_regex_entities

    # Check Analyser
    if not analyser:
        analyser = create_analyser(
            model_path=model_path,
            spacy_model=spacy_model,
            language=language,
            regex_entities=regex_entities,
        )
    else:
        if rebuild_regex_recognisers:
            rebuild_analyser_regex_recognisers(
                analyser=analyser, regex_entities=regex_entities
            )

    # Analyse the text
    initial_results = analyse(
        text,
        analyser,
        entities=entities,
        regex_entities=regex_entities,
        mask_individual_words=mask_individual_words,
        text_separator=text_separator,
        rebuild_regex_recognisers=False,
        **kwargs,
    )

    # Create an OperatorConfig that randomly selects replacements from the replacement list
    operator_config = None
    if entities:
        if replacement_lists:
            operator_config = {}
            for entity in entities:
                if entity in replacement_lists:
                    operator_config[entity] = OperatorConfig(
                        "replace",
                        {"new_value": random.choice(replacement_lists[entity])},
                    )

    # Anonymise the text
    anonymiser = AnonymizerEngine()

    # if-else is strictly required as the anonymize method modifies initial_results variable when called
    if not mask_individual_words:
        anonymized_result = anonymiser.anonymize(
            text=text, analyzer_results=initial_results, operators=operator_config
        )
    else:
        # this is essentially AnonymizerEngine.anonymize without merging adjacent entities of the same type
        # some discussion around merging adjacent entities: https://github.com/microsoft/presidio/issues/1090
        analyzer_results = anonymiser._remove_conflicts_and_get_text_manipulation_data(
            initial_results, ConflictResolutionStrategy.MERGE_SIMILAR_OR_CONTAINED
        )
        operators = anonymiser._AnonymizerEngine__check_or_add_default_operator(
            operator_config
        )
        anonymized_result = anonymiser._operate(
            text, analyzer_results, operators, OperatorType.Anonymize
        )

    # TODO - could be managed by creating an Operatorconfig for "PHONE_NUMBER"
    anonymised_text = anonymized_result.text.replace("PHONE_NUMBER", "NUMBER")

    return highlight_text(anonymised_text) if highlight else anonymised_text


def anonymise_df(
    df: pd.DataFrame,
    column: str | list[str],
    analyser: AnalyzerEngine | None = None,
    entities: list[str] = DEFAULT_ENTITIES,
    regex_entities: Sequence[str | PteredactylRecogniser] = DEFAULT_REGEX_ENTITIES,
    highlight: bool = False,
    replacement_lists: dict | None = None,
    inplace: bool = False,
    model_path: str = None,
    spacy_model: str = DEFAULT_SPACY_MODEL,
    language: str = "en",
    mask_individual_words: bool = False,
    text_separator: str = " ",
    col_inplace: bool = False,
    col_header_append: str = "_redacted",
    rebuild_regex_recognisers: bool = True,
    **kwargs,
) -> pd.DataFrame:
    """
    Anonymises the given text by replacing specified entities by NER, and and regex entities by REGEX. Regex entities take priority and are analysed first.
    It is recommended to first create an analyser and feed this in to be reused.

    Args:
    df (DataFrame): The DataFrame to anonymise.
    column (str or list): The column(s) to anonymise.
    analyser (AnalyzerEngine, optional): An instance of AnalyzerEngine. If not provided, a new analyser will be created.
    entities (list, optional): A list of entity types to anonymize. If not provided, a default list will be used.
    regex_entities (list, optional): A list of regex entities or PteredactylRecognisers to analyse. If not provided, a default list will be used.
    highlight (bool): If True, highlights the anonymized parts in the text.
    replacement_lists: (dict, optional): A dictionary with entity types as keys and lists of replacement values for hide-in-plain-sight redaction.
    model_path (str): The path to the model used for analysis. Used only if analyser not provided.
    spacy_model (str): The spaCy model to use. Used only if analyser not provided.
    language (str): The language of the text to be analyzed. Defaults to "en". Used only if analyser not provided.
    mask_individual_words (bool): If True, prevents joining of next-door entities together.
            (i.e. Jane Smith becomes <PERSON> <PERSON> if True, or <PERSON> if False). Defaults to False.
    text_separator (str): Text separator. Default is whitespace.
    inplace (bool): If True, modifies the DataFrame in place. If False, copies the DataFrame and modifies the copy.
    col_inplace (bool): If True, replaces the original column with the anonymized column. If False, returns anonymised text in a new column.
    col_header_append (str): String to append to the header of the anonymised column.
    rebuild_regex_recognisers (bool): If True, and an existing analyser is provided, the analyser's regex recognisers will be rebuilt before execution.
    **kwargs: Additional keyword arguments for analyse.

    Returns:
    DataFrame: The anonymized DataFrame.
    """

    # Check Analyser
    if not analyser:
        analyser = create_analyser(
            model_path=model_path,
            spacy_model=spacy_model,
            language=language,
            regex_entities=regex_entities,
        )
    else:
        if rebuild_regex_recognisers:
            rebuild_analyser_regex_recognisers(
                analyser=analyser, regex_entities=regex_entities
            )

    # Prepare
    if type(column) not in [str, list]:
        raise TypeError("column argument must be a string or list of strings")

    columns = [column] if isinstance(column, str) else column

    if not inplace:
        df = copy.copy(df)

    def anonymize_row(text: str) -> str:
        return anonymise(
            text,
            analyser=analyser,
            highlight=highlight,
            entities=entities,
            regex_entities=regex_entities,
            replacement_lists=replacement_lists,
            mask_individual_words=mask_individual_words,
            text_separator=text_separator,
            rebuild_regex_recognisers=False,
            **kwargs,
        )

    for col in tqdm(columns):
        new_col = f"{col}{col_header_append}"
        tqdm.pandas(desc=f"Redacting '{col}'")
        df[new_col] = df[col].progress_apply(anonymize_row)

        if col_inplace:
            df[col] = df[new_col]
            df.drop(columns=[new_col], inplace=True)

    return df
