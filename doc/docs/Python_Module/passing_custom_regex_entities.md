We can include custom regex and check functions in our analysis/redaction, too:

```python
import pteredactyl as pt
from pteredactyl import build_pteredactyl_recogniser

# Create an analyser
analyser = pt.create_analyser()

# Build a custom regex recogniser
def check_soton_landline(input: str):
    cleaned = input.replace('-','').replace(' ','')
    return cleaned.startswith('0238')


soton_landline_recogniser = build_pteredactyl_recogniser(entity_type = 'SOUTHAMPTON_LANDLINE',
                                           regex = r'(?:\d[\s-]?){11}',
                                           check_function = check_soton_landline)

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024. He can be contacted at 02380 111111"
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True, entities="PERSON", regex_entities=["NHS_NUMBER", "POSTCODE", soton_landline_recogniser])

print(redacted_text)
```
```Output
The patient's name is <PERSON>. His NHS Number is <NHS_NUMBER> and postcode is <POSTCODE>. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024. He can be contacted at <SOUTHAMPTON_LANDLINE>
```
