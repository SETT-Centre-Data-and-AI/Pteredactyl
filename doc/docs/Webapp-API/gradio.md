The source code for the web app and API can be found here [Pteredactyl_Gradio_Web_App](https://github.com/MattStammers/Pteredactyl/tree/main/src/pteredactyl_webapp).

### Deploying Gradio App from source

To deploy a gradio app is fairly simple. First clone the git repository:

```sh
git clone {git repo}
```

Then navigate into the src/pteredactyl_webapp directory and making sure poetry is installed first set up the poetry venv as follows:

```sh
poetry shell
poetry install
```

Then to run the app you call

```sh
python app.py
```

and the app will run. If you want to see the gradio-deployed production version you can play with it here:

This webapp is already available online as a gradio app on Huggingface: [Huggingface Gradio App](https://huggingface.co/spaces/MattStammers/pteredactyl_PII).
