<h1 align="center">
<br>Pteredactyl Documentation <br>
<img src="https://github.com/MattStammers/Pteredactyl/raw/main/src/pteredactyl_webapp/assets/img/Pteredactyl_Logo.jpg" alt="Pteredactyl Logo" width="500">
</h1>

# Pteredactyl Python Module, Gradio Webapp, API

- Authors: Matt Stammers🧪, Cai Davis🥼 and Michael George🩺

- Version 1. 29/06/2024

Clinical patient identifiable information (cPII) presents a significant challenge in natural language processing (NLP) that has yet to be fully resolved but significant progress is being made [1,2].

This is why we created [Pteredactyl](https://pypi.org/project/pteredactyl/) - a python module to help with redaction of clinical free text.

## Pteredactyl Documentation

Welcome to the official documentation for Pteredactyl, a comprehensive tool for redacting clinical free text. This documentation covers the usage and development of the Pteredactyl Python Module, Gradio Webapp, and API.

## Purpose

Clinical patient identifiable information (cPII) presents a significant challenge in natural language processing (NLP). Pteredactyl is designed to address this challenge by assisting with the redaction of cPII from clinical free text using advanced NLP techniques.

## Features

- **Python Module**: Easily integrate Pteredactyl into your projects to redact cPII from text.
- **Gradio Web App**: User-friendly web interface for redaction tasks.
- **API**: Deployable API for seamless integration into other systems.

## Quick Links

- [Quickstart](Python Module/quickstart.md): Get started with Pteredactyl quickly.
- [Webapp/API](webapp-api.md): Access and use the Gradio Webapp and API.
- [Developing/Contributing](developing-contributing.md): Learn how to contribute to the project.
- [License](license.md): Information about the project's license.

## Tool Usage Instructions

When the input text is entered, the tool redacts the cPII using NLP with labeled masking tokens and assesses the model's results. You can test the text against different models by selecting from the dropdown menu.

## Python Module

The source code for the python module can be accessed here: [Pteredactyl Python Module](https://github.com/MattStammers/Pteredactyl/tree/main/src/pteredactyl). Contributions to further develop the module are welcome.

## Gradio Web App

The source code for the web app and API can be found here: [Pteredactyl_Gradio_Web_App](https://github.com/MattStammers/Pteredactyl/tree/main/src/pteredactyl_webapp)

This is so that other NHS and healthcare sites can deploy this on premesis or in the cloud as a standalone python module is not as useful as a webapp/api to most NHS/Healthcare users.

This webapp is already available online as a gradio app on Huggingface: [Huggingface Gradio App](https://huggingface.co/spaces/MattStammers/pteredactyl_PII). It is also available as [source](https://github.com/SETT-Centre-Data-and-AI/PteRedactyl) or as a Docker Image: [Docker Image](https://registry.hub.docker.com/r/mattstammers/pteredactyl). All are MIT licensed.

## Docker Deployment

Please note if deploying the docker image the port bindings are to 7860. The image can also be deployed from source using the following command:

```bat
docker build -t pteredactyl:latest .
docker run -d -p 7860:7860 --name pteredactyl-app pteredactyl:latest
```

Or can be deployed directly from [Docker Hub](https://registry.hub.docker.com/r/mattstammers/pteredactyl)

## Usage

To use Pteredactyl, access the provided tools and documentation to redact cPII from clinical free text using the Python module, Gradio web app, or API. Details for setup and usage can be found in the [Quickstart](quickstart.md) section.

For access to the dashboard, please refer to the [Webapp/API](webapp-api.md) section.

[Docs Version](./version.md#version)
