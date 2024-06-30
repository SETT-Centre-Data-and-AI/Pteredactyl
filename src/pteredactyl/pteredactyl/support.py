import re
from collections.abc import Sequence
from logging import Logger
from typing import Any

import spacy
from presidio_analyzer import RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine, NlpEngineProvider
from presidio_analyzer.recognizer_result import RecognizerResult

from pteredactyl.defaults import SPACY_LABELS_TO_IGNORE
from pteredactyl.recognisers.pteredactyl_recogniser import (
    PTEREDACTYL_RECOGNISER_NAME,
    PteredactylRecogniser,
)
from pteredactyl.recognisers.support import _get_config
from pteredactyl.recognisers.transformers_recogniser import TransformersRecogniser
from pteredactyl.regex_entities import fetch_pteredactyl_recogniser


def find_substring_positions(s: str, sep: str = " ") -> list[tuple[int, int]]:
    """Finds the starting and ending indexes of substrings in the input string `s`.
    The substrings are determined by splitting `s` at separator.

    Args:
        s (str): The input string containing substrings separated by newlines.
        sept (str): Separator for substrings.

    Returns:
        list[tuple[int, int]]: A list of tuples, each containing the start and end index of a substring.

    Examples:
    >>> s = "abc\ndef"
    >>> positions = find_substring_positions(s, sep="\n")
    >>> print("Replacement Positions: ", positions)
    Replacement Positions: [(0, 3), (4, 7)]
    """
    replacement_positions = []

    for substring in s.split(sep):
        for match in re.finditer(re.escape(substring), s):
            start, end = match.span()
            replacement_positions.append((start, end))

    return replacement_positions


def split_results_into_individual_words(
    text: str, results: list[RecognizerResult], text_separator: str = " "
) -> list[RecognizerResult]:
    """
    Splits identified RecognizerResults into individual words. For example, Jane Smith becomes <PERSON> <PERSON>, rather than <PERSON>.

    Args:
        text (str): The text that was analyzed.
        results (list[RecognizerResult]): The results of the analysis.
        text_separator (str): The separator used to split the text into individual words.

    Returns:
        list[RecognizerResult]: A list of RecognizerResults, each representing an individual word.
    """
    masked_individual_words_results = []
    for result in results:
        substrings = text[result.start : result.end]
        for substring_position in find_substring_positions(
            substrings, sep=text_separator
        ):
            offset = result.start
            masked_individual_words_results.append(
                RecognizerResult(
                    entity_type=result.entity_type,
                    start=substring_position[0] + offset,
                    end=substring_position[1] + offset,
                    score=result.score,
                    analysis_explanation=result.analysis_explanation,
                    recognition_metadata=result.recognition_metadata,
                )
            )
    return masked_individual_words_results


def return_allowed_results(
    initial_results: list[RecognizerResult],
    allowed_entities: list[str],
    allowed_regex_entities: list[str],
) -> list[RecognizerResult]:
    """
    Checks list of RecognizerResults for allowed entities returns a list of allowed results.

    Args:
        initial_results (list[RecognizerResult]): The list of RecognizerResults to filter.
        allowed_entities (list[str]): The list of entity types to allow.
        allowed_regex_entities (list[str]): The list of regex entity types to allow.

    Returns:
        list[RecognizerResult]: The filtered list of RecognizerResults.
    """
    results = []
    for result in initial_results:
        recogniser = result.recognition_metadata["recognizer_name"]
        entity_type = result.entity_type

        if recogniser == PTEREDACTYL_RECOGNISER_NAME:
            if entity_type in allowed_regex_entities:
                results.append(result)
        else:
            if entity_type in allowed_entities:
                results.append(result)

    return results


def highlight_match(match: re.Match[str]) -> str:
    word = match.group(1)
    return f"\033[1m\033[33m<{word}>\033[0m"


def highlight_text(input_text: str) -> str:
    pattern = r"<(.*?)>"
    return re.sub(pattern, highlight_match, input_text)


def load_spacy_model(spacy_model: str) -> None:
    """Downloads spacy model if not already installed

    Args:
        spacy_model (str): Name of spacy model
    """
    if not spacy.util.is_package(spacy_model):
        print(f"Downloading model '{spacy_model}' for the first time, please wait...")
        spacy.cli.download(spacy_model)


def load_transformers_recognizer(model_path: str) -> TransformersRecogniser:
    """Loads transformers recognizer with the specified model path

    Args:
        model_path (str): Path to the transformer model

    Returns:
        TransformersRecogniser: Loaded transformers recognizer
    """
    print(f"Loading transformers recognizer with model path: {model_path}")
    config = _get_config(model_path=model_path)
    transformers_recognizer = TransformersRecogniser(model_path=model_path)
    transformers_recognizer.load_transformer(**config)
    print(f"Model {model_path} loaded successfully")
    return transformers_recognizer


def load_nlp_configuration(language: str, spacy_model: str) -> dict[str, Any]:
    """Loads NLP configuration for spacy model

    Args:
        language (str): Model language (e.g. en)
        spacy_model (str): Name of spacy model (e.g. en_core_web_sm)

    Returns:
        dict: configuration dictionary that can be passed to create an NlpEngineProvider
    """
    return {
        "nlp_engine_name": "spacy",
        "models": [
            {
                "lang_code": language,
                "model_name": spacy_model,
            }
        ],
        "ner_model_configuration": {"labels_to_ignore": SPACY_LABELS_TO_IGNORE},
    }


def load_registry(
    transformers_recogniser: TransformersRecogniser,
    regex_entities: Sequence[str | PteredactylRecogniser],
) -> RecognizerRegistry:
    """Creates an AnalyzerEngine.registry by combining a TransformersRecogniser with a list of custom PteredactylRecognisers

    Args:
        transformers_recogniser (TransformersRecogniser): Custom transformers recogniser
        regex_entities (list[str | PteredactylRecogniser]): Named regex entities to generate PtereractylRecognisers, or custom PtereractylRecognisers

    Returns:
        RecognizerRegistry: registry of Recognisers for an AnalyzerEngine
    """
    registry = RecognizerRegistry()
    # registry.load_predefined_recognizers() # Presidio default recognizers - largely not needed
    registry.add_recognizer(transformers_recogniser)
    registry.remove_recognizer("SpacyRecognizer")

    if regex_entities:
        for entity in regex_entities:
            if isinstance(entity, str):
                recogniser = fetch_pteredactyl_recogniser(entity_type=entity)
            elif isinstance(entity, PteredactylRecogniser):
                recogniser = entity
            registry.add_recognizer(recogniser)

    return registry


def load_nlp_engine(
    presidio_logger: Logger, nlp_configuration: dict[str, Any]
) -> NlpEngine:
    """
    Loads a NlpEngineProvider by creating a new engine.

    Args:
        presidio_logger (Logger): Logger object to set and restore logging level.
        nlp_configuration (dict): Configuration for the NlpEngineProvider.

    Returns:
        NlpEngineProvider: The loaded engine.
    """
    log_level = presidio_logger.level
    presidio_logger.setLevel("ERROR")
    nlp_engine = NlpEngineProvider(nlp_configuration=nlp_configuration).create_engine()
    presidio_logger.setLevel(log_level)

    return nlp_engine
