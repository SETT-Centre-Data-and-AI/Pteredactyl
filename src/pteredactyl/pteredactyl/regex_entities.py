import re
from collections.abc import Callable, Sequence
from pathlib import Path

from presidio_analyzer import AnalyzerEngine

from pteredactyl.exceptions import MissingRegexRecogniserError
from pteredactyl.recognisers.pteredactyl_recogniser import (
    PTEREDACTYL_RECOGNISER_NAME,
    PteredactylRecogniser,
)
from pteredactyl.regex_check_functions import is_nhs_number

REGEX_ENTITIES = {
    # entity_type: (regex, check_function)
    "NHS_NUMBER": (r"\d(?:[\s-]?\d){9,}", is_nhs_number),
    "POSTCODE": (r"[A-Z]{1,2}[0-9R][0-9A-Z]?\s?[0-9][A-Z]{2}", None),
    "EMAIL_ADDRESS": (r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", None),
}


def build_pteredactyl_recogniser(
    entity_type: str,
    regex: str | re.Pattern,
    check_function: Callable[..., bool] | None,
) -> PteredactylRecogniser:
    """
    Build a custom regex ptererecogniser for pteredactyl.

    Args:
        entity_type (str): The name of the entity to be recognised.
        regex (str or re.Pattern): The regular expression to match the entity.
        check_function (Callable, optional): A function to check if the matched string is a valid entity. Should take a single argument (the matched string) and return a boolean.

    Returns:
        PteredactylRecogniser: A custom presidio EntityRecognizer object.

    Example:
    >>> def check_soton_landline(input: str):
    ... cleaned = input.replace('-','').replace(' ','')
    ... return cleaned.startswith('0238')


    >>> recogniser = build_pteredactyl_recogniser(entity_type='SOUTHAMPTON_LANDLINE',
    ...                                           regex=r'(?:\\d[\\s-]?){11}',
    ...                                           check_function=check_soton_landline)
    """

    regex = re.compile(regex) if isinstance(regex, str) else regex
    return PteredactylRecogniser(
        entity_type=entity_type, regex=regex, check_function=check_function
    )


def fetch_pteredactyl_recogniser(entity_type: str) -> PteredactylRecogniser:
    if entity_type not in REGEX_ENTITIES.keys():
        raise MissingRegexRecogniserError(
            f"""Entity '{entity_type}' not found. Consider adding to the 'REGEX_ENTITIES' dictionary, or feeding a custom recogniser to regex_entities with:
 -> from pteredactyl.{Path(__file__).stem} import build_pteredactyl_recogniser
 -> recogniser = build_pteredactyl_recogniser(entity_type='{entity_type}', regex=r'some_regex', check_function=None) # or create a check_function with a single input argument, returning either True (correct match) or False"""
        )

    return build_pteredactyl_recogniser(
        entity_type=entity_type,
        regex=REGEX_ENTITIES[entity_type][0],
        check_function=REGEX_ENTITIES[entity_type][1],
    )


def build_regex_entity_recogniser_list(
    regex_entities: str | PteredactylRecogniser | Sequence[str | PteredactylRecogniser],
) -> list[PteredactylRecogniser]:
    """
    Build a list of custom regex PteredactylRecognisers.

    Args:
        regex_entities (list[str or PteredactylRecogniser]): A list of PteredactylRecogniser objects or strings referencing pre-built PteredactylRecognisers.

    Returns:
        list[PteredactylRecogniser]: A list of custom presidio EntityRecognizer objects.

    Example:
    >>> recognisers = build_regex_entity_recogniser_list(['NHS_NUMBER',
    ...                                                    'ENTITY_2',
    ...                                                    PteredactylRecogniser(entity_type='SOUTHAMPTON_LANDLINE',
    ...                                                                          regex=r'\\b((?:\\+44\\s?7\\d{3}|\\(?07\\d{3}\\)?)\\s?\\d{3}\\s?\\d{3}|\\(?01\\d{1,4}\\)?\\s?\\d{1,4}\\s?\\d{1,4})\\b',
    ...                                                                          check_function=check_so_landline
    ...                                                   ])
    """

    regex_entity_recognisers = []
    if type(regex_entities) in (str, PteredactylRecogniser):
        regex_entities = [regex_entities]

    for regex_entity in regex_entities:
        if isinstance(regex_entity, str):
            regex_entity_recognisers.append(
                fetch_pteredactyl_recogniser(entity_type=regex_entity)
            )
        else:
            regex_entity_recognisers.append(regex_entity)

    return regex_entity_recognisers


def rebuild_analyser_regex_recognisers(
    analyser: AnalyzerEngine, regex_entities: Sequence[str | PteredactylRecogniser]
) -> None:
    """
    Rebuilds the analyser's regex recognisers with the supplied list of regex entities.

    Args:
        analyser (AnalyzerEngine): The analyser to rebuild.
        regex_entities (list[str or PteredactylRecogniser]): The list of regex entities to use.

    Returns:
    """

    analyser.registry.remove_recognizer(PTEREDACTYL_RECOGNISER_NAME)
    pteredactyl_recognisers = build_regex_entity_recogniser_list(regex_entities)
    for recogniser in pteredactyl_recognisers:
        analyser.registry.add_recognizer(recogniser)
