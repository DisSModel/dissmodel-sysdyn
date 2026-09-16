FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up a new user to avoid running as root
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user demo/requirements.txt ./demo/requirements.txt
RUN pip install --no-cache-dir -r demo/requirements.txt

COPY --chown=user pyproject.toml README.md ./
COPY --chown=user src ./src
COPY --chown=user demo/app.py ./demo/app.py

RUN pip install --no-cache-dir .

# Expose the port Streamlit will run on (Hugging Face uses 7860)
EXPOSE 7860

# Command to run the app
CMD ["streamlit", "run", "demo/app.py", "--server.port", "7860", "--server.address", "0.0.0.0"]
