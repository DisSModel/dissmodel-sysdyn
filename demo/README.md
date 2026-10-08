---
title: DisSModel System Dynamics Explorer
emoji: 📈
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
license: mit
short_description: Run the dissmodel-sysdyn models in the browser
---

# System Dynamics Explorer

Interactive demo of [dissmodel-sysdyn](https://github.com/DisSModel/dissmodel-sysdyn):
pick a model (SIR, predator–prey, Lorenz, Daisyworld…), set its parameters in
the sidebar and watch the stocks evolve.

This folder is self-contained and is what gets deployed:

```bash
# locally
pip install -r requirements.txt
streamlit run app.py

# or with Docker
docker build -t sysdyn-demo . && docker run -p 7860:7860 sysdyn-demo
```

To publish on Hugging Face, create a Space with the Docker SDK and push the
contents of this folder to it. The header above is the Space configuration.
