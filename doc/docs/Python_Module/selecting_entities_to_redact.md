We can select specific NER or regex entities to analyse/redact by feeding in these arguments. When empty, PteRedactyl will redact according to a predefined list, which can be checked as follows:

```python
import pteredactyl as pt
pt.show_defaults()
```

Let's try redacting only specific entities:

```python
import pteredactyl as pt

# Create an analyser
analyser = pt.create_analyser()

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024."
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True)

print(redacted_text)

# Redact specific entities - keeping the date
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024."
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True, entities="PERSON", regex_entities=["NHS_NUMBER", "POSTCODE"])

print(redacted_text)
```
