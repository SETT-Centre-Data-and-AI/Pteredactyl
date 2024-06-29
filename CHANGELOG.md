## v1.0.0 (2024-06-29)

### Feat

- **Gradio**: Gradio app added to allow deployment as an API and webapp
- **Dockerfile**: Deployment inside containers for production API deployment
- **Public Pypi installable**: Deployment to public PyPi to make openly installable
- **Open Source Test Challenge Deployment**: Added open source test challenge for the OHSDI community to take on
- **Logging added**: Logging added

### Refactor

- **documentation**: Documentation edited to make it easier for new users to understand and implement
- **dependencies**: Revised dependencies to reduce future depreciation / security risks

## v0.5.0 (2024-05-31)

### Feat

- **redactor**: added special_entities to redactor
- **special_entities**: added redact_special_matches
- **special_entities**: postcodes implemented with tests
- **special_entities**: refacted to support multiple regex matches, and refactored tests
- **SpecialMatch**: added match, and wrote test for find_nhs_number
- **special_entities.py**: added special_entities.py and functions to find nhs numbers and replace in text
- **support_classes.py**: Added support_classes and SpecialMatch
- **support.py**: added is_nhs_number check

### Refactor

- **special_entities**: renamed redact_special_matches to redact_special_entities

## v0.4.2 (2024-05-31)
- **major**: Add a param to allow masking individual words
- **pyproject.toml**: remove rds source

## v0.4.1 (2024-05-28)

## v0.4.0 (2024-05-28)

### Feat

- **major**: major tweaks to argument passing and build
- **pyproject.toml**: restored poetry source
- **poetry-install**: fixed from server - removed empty pteredactyl folder
- **poetry-lock**: updated poetry lock

## v0.3.0 (2024-03-18)

### Feat

- **analyze-function**: added support for custom entities within the analyze function of support.py file

## v0.2.0 (2024-01-03)

### Feat

- **redactor.py**: Added replacement list to the anonymiser to allow replacement of entities based on a predefined list

### Fix

- **dependencies**: added IProgress, ipywidgets, and ipykernel to dependencies

### Refactor

- **gitignore**: added dist to gitignore
- **General**: several files cleaned up
- **Folder-structure**: added src/ directory and moved pterydactyl code here
- **poetry**: added commit and amended pyproject
