import re
from collections.abc import Callable
from typing import Optional

from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts

PTEREDACTYL_RECOGNISER_NAME = "PteredactylRecogniser"


class PteredactylRecogniser(EntityRecognizer):
    """
    PteredactylRecognizer is a Rule based logic recognizer that identifies entities
    in a given text using regular expressions. Optionally, a custom check function
    can be used to further validate the matches.

    Args:
        entity_type (str): The type of entity to recognize.
        regex (str): The regular expression pattern used to identify entities.
        check_function (Optional[Callable]): An optional function to further validate matches.
        expected_confidence_level (float): The confidence level assigned to recognized entities.

    Example:
        >>> from pteredactyl.support import is_nhs_number
        >>> nhs_numbers_recognizer = PteredactylRecognizer(
        ...     entity_type="NHS_NUMBER",
        ...     regex=r"\\d(?:[\\s-]?\\d){9,}",
        ...     check_function=is_nhs_number,
        ...     supported_entities=["NHS_NUMBER"],
        ... )
        >>> analyser.registry.add_recognizer(nhs_numbers_recognizer)
    """

    def __init__(
        self,
        entity_type: str,
        regex: str | re.Pattern,
        check_function: Optional[Callable] = None,
        supported_entities: Optional[list[str]] = None,
        expected_confidence_level: float = 1.5,
    ):
        self.entity_type = entity_type
        self.regex = regex if isinstance(regex, re.Pattern) else re.compile(regex)
        self.check_function = check_function
        self.supported_entities = (
            supported_entities if supported_entities is not None else [entity_type]
        )
        self.expected_confidence_level = expected_confidence_level
        super().__init__(supported_entities=self.supported_entities)

    def load(self) -> None:
        """No loading is required."""
        pass

    def analyze(
        self, text: str, entities: list[str], nlp_artifacts: NlpArtifacts
    ) -> list[RecognizerResult]:
        """
        Analyzes text to find tokens that match the provided regex pattern and optionally
        checks them with a custom check function.
        """
        results = []
        for match in self.regex.finditer(text):
            if not self.check_function or self.check_function(match.group()):
                result = RecognizerResult(
                    entity_type=self.entity_type,
                    start=match.start(),
                    end=match.end(),
                    score=self.expected_confidence_level,
                )
                results.append(result)

        return results
