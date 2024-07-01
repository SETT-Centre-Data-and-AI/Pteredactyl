When analysing or anonymising multiple pieces of text or DataFrames in the same way, it is highly recommended to create and reuse a single analyser (presidio AnalyzerEngine). While each high-level PteRedactyl function will spin up an analyser if one is not provided, an analyser can be created and then passed, to reuse it.

Example Usage:
```python
import pteredactyl as pt

# Create an analyser
analyser = pt.create_analyser()

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True)

print(redacted_text)
```
