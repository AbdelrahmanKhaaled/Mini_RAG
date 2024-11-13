# Mini_RAG

This is minimal implementation of the RAG model for question answering.

## Requirments

- Python 3.8 or later

### Install Python using MiniConda

1) Download and install miniconda from [here](https://docs.anaconda.com/miniconda/#quick-command-line-install)

2) Create new environment using the following command:
```bash
$ conda creat -n mini-rag-app python=3.8
```

2) Activate the environment:
```bash
$ conda activate mini-rag-app
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Installation the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. like `OPENAI_API_KEY` value