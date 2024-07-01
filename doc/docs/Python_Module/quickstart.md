Here is a hello world quickstart deployment to get anyone going with Pteredactyl

```python
# Simple anonymisation
import pteredactyl as pt
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"

anonymised_text = pt.anonymise(text)
```

You can also configure the package by passing different parameters:

- `entities`: List of entities to anonymise.
- `replacement_lists`: Custom replacement values for each entity.
- `highlight`: Set to `True` to highlight anonymised parts in the output.

```python

# Anonymisation for specific entities
entities = ["LOCATION", "PERSON"]
anonymised_text = pt.anonymise(text, entities=entities)

# Hide in plain site by supplying a dictionary of entities: potential replacements
replacement_lists = {
    "PERSON": ["Alice Smith", "Bob Johnson", "Carol Davis"],
    "LOCATION": ["Los Angeles", "Chicago", "Houston"]
}
anonymised_text = pt.anonymise(text, replacement_lists=replacement_lists)
```
