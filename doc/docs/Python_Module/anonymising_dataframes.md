The `anonymise_df()` function is designed to anonymise sensitive information in a pandas DataFrame. This function can handle Named Entity Recognition (NER) and regex-based entity recognition to redact information such as names, addresses, and other personal identifiers. It can act on a single column or multiple, and redact inplace or by returning a new DataFrame/column

### Parameters

- `df`: The DataFrame containing the text to anonymise.
- `column`: The name or list of names of the column(s) to anonymise.
- `analyser`: An optional AnalyzerEngine instance. If not provided, a new analyser will be created.
- `entities`: A list of entities to anonymise using the NER model.
- `regex_entities`: A list of regex patterns or custom recognisers to identify and anonymise.
- `highlight`: If `True`, anonymised parts are highlighted.
- `replacement_lists`: A dictionary for hide-in-plain-sight redaction containing replacement values per entity type.
- `inplace`: If `True`, the original DataFrame is modified; otherwise, a copy is returned.
- `col_inplace`: If `True`, the original column is replaced with the redacted version.

### Basic Example

Here's a basic example of anonymising a DataFrame column:

```python
import pandas as pd
import pteredactyl as pt

analyser = pt.create_analyser()

# Create a DataFrame with sample data
df = pd.DataFrame({
    'text': [
        "John Doe's number is 07111 293892.",
        "Jane Smith's lives at 123 Shirley Road."
    ]
})

# Anonymise the 'text' column
anonymised_df = pt.anonymise_df(
    df=df,
    column='text',
    analyser=analyser,
    entities=['PERSON', 'PHONE_NUMBER', 'LOCATION'],
    inplace=False
)

# Print the result
print(anonymised_df)
```
```Output
                                      text                       text_redacted
0       John Doe's number is 07111 293892.  <PERSON>'s number is 07111 293892.
1  Jane Smith's lives at 123 Shirley Road.     <PERSON>'s lives at <LOCATION>.
```
