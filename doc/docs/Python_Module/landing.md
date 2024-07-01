PteRedactyl is a redaction package for personally identifiable information (PII) in text, that combines NER models with regex matching to identify and mask sensitive information. Custom transformers-based NER models can be swapped in,

This guide will cover usage of PteRedactyl's main functions: `create_analyser`, `analyse`, `anonymise` and `anonymise_df`:

- `create_analyser()`: Creates a presidio AnalyserEngine that can be reused across high-level functions
- `analyse()`: Analyses a string for PII, returning a list of recognised NER or regex-based results with scores
- `anonymise()`: Analyses and anonymises text, replacing PII with placeholders or hide-in-plain-sight (HIPS) replacements
- `anonymise_df()`: As above, but by looping over a given column (or columns) in a DataFrame
