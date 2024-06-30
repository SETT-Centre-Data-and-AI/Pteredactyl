# Pteredactyl

_Pteredactyl utilizes advanced natural language processing techniques to identify and anonymize clinical personally identifiable information (cPII) in clinical free text. It is built on top of Microsoft's [Presidio](https://microsoft.github.io/presidio/) and allows interchange of various transformer models from [Huggingface](https://huggingface.co/)_

## Features

- Anonymization of various entities such as names, locations, and phone numbers
- Support for processing both strings and pandas DataFrames
- Text highlighting for easy identification of anonymized parts
- Webapp with [Gradio](https://huggingface.co/spaces/MattStammers/pteredactyl_PII)
- cPII benchmarking test: [Clinical_PII_Redaction_Test](https://huggingface.co/datasets/MattStammers/Clinical_PII_Redaction_Test)
- Production API deployed using [Docker](https://www.docker.com/) and [Gradio](https://www.gradio.app/)
- Hide in plain site replacement or masking option

## Installation

Can be installed using pip from PyPi:

```bash
pip install pteredactyl
```

## Guides

* [User Guide](./documentation/user-guide.md)

## Contributions
Interested in contributing? Check out the contributing guidelines.

* [Developer Guide](CONTRIBUTING.md)

Please note that this project follows the [Github code of conduct](https://docs.github.com/en/site-policy/github-terms/github-community-code-of-conduct). By contributing to this project, you agree to abide by its terms.

## License
Pteredactyl was created at University Hospital Southampton NHSFT by the Research Data Science Team. It is licensed under the terms of the MIT license.
