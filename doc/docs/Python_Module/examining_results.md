Instead of anonymising, we can instead check the results of analysis by using the `analyse()` function.

```python
import pteredactyl as pt

text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"
analyser = pt.create_analyser()
analysis = pt.analyse(text=text, analyser=analyser)
for result in analysis:
    print(result)
```
