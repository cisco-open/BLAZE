# BLAZE - Building Language Applications with eaZE 

> [BLAZE Drag-and-Drop - README](drag/README.md) | [BLAZE Conversational AI - README](conv/README.md)

&nbsp;&nbsp;

The goal of BLAZE is to **make the lives of data scientists easier**, filling-in a required niche. 

Natural Language Processing (NLP) pipelines reuse many of the same components arranged in different orders. The purpose each NLP model serves varies from use-case to use-case. However, these NLP models are not standardized in terms of their inputs, outputs, and hardware requirements. As a result, it is very difficult to interchange and combine NLP models, especially without introducing significant amounts of code. This lack of standardization causes NLP pipelines to be very rigid. Their lack of flexibility makes it difficult to compose, modify, and add functionality. 

To solve this problem, Blaze that allows for the modular creation and composition of NLP pipelines. Each component of the NLP Pipeline can be implemented as "building block" (for example, a microservice). These building blocks will have standardized inputs and outputs, and they can easily be assembled in varying orders. The order and choice of these specific blocks result in varying pipelines, built for unique use-cases.

BLAZE is a pipeline creation framework, into which other external models and libraries can be incorporated. In the following sections of the Readme, we showcase how to install and use BLAZE with external libraries like ElasticSearch, ColBERT and the WebEx Mindmeld libraries. The instructions to install and run these libraries are highlighted in the respective sections too. 


## Features 

Here's BLAZE's current functionalities:

**Use Case #1 - Developer** 

- **Drag-and-Drop Pipeline Builder** 
  - Visual builder for configuring and deploying pipelines
  - Allows for building from scratch (adding, connecting components)
  - Allows for uploading existing pipelines (visualize "recipes") 
  - Converts custom recipe into downloadable YAML config file 
  - Generates and launches custom NLP pipeline solution 

- **Conversational AI (Webex Bot)** 
  - Interface with BLAZE to specify pipeline components
  - Generate and launch custom NLP pipeline solution 

  &nbsp;&nbsp;

**Use Case #2 - Business** 

- **Visual Dashboard Web App** 
  - Visual representation of generated pipeline
  - Supports semantic search, summarization, file upload, etc. 

- **Conversational AI (Webex Bot)** 
  - Interact with generated pipeline through natural language
  - Can choose knowledge base (ex. upload file, view all files) 
  - Can index model and retrieve results (ex. summarize this doc) 
  - Can retrieve knowledge base, model, and metrics info 

  &nbsp;&nbsp;

**Use Case #3 - Researcher** 

- **Model/Knowledge Base Benchmarking** 
  - Benchmark selected model on selected knowledge base 
  - Gives latency (avg time/question, as well as generates real-time graph)
  - Gives accuracy (num correct, num total, % correct, % progress) 
  - Displays incorrect questions 

- **Model/Knowledge Base Comparison** 
  - Benchmark multiple models on selected knowledge base 
  - Gives latency (avg time/question, as well as generates real-time graph)
  - Gives side-by-side accuracy (num correct, num total, % correct, % progress) 
  - Displays incorrect questions 

- **Model/Knowledge Base Metrics** 
  - Compute and display scientific metrics 
  - Currently Supported Metrics: BertScore, Bleu, Rouge 

  &nbsp;&nbsp;

> GIFS/Screenshots Coming Soon! 

  ![Custom](./docs/custom_qna.PNG)

  ![Comparison](./docs/model_comparison.png)



> Over the coming weeks, this platform will be further fleshed out with more exciting features 😄. 


&nbsp;&nbsp;

## Installing Locally
## Installation 

First, clone this repository by running:

`git clone https://wwwin-github.cisco.com/jasriniv/blaze.git`

Install faiss-gpu with

`conda install -c pytorch faiss-gpu`

 Next, create your conda environment with 

`conda env create -f aski_env.yml`

Then, activate your conda environment with 

`conda activate aski`

Ensure that your elasticsearch client is up and running. For more information, see "Supported Models" section. 
Wait for ElasticSearch to load and ensure that your elasticsearch client is up and running. For more information, see 
"Supported Models" section. Finally, run the dashboard with: 

`python build.py`

Now, a link should appear (ex. `Dash is running on http://127.0.0.1:5010/`). Run this link in your browser to open the dashboard! 

You can use the dashboard to create your own NLP Pipeline !!

&nbsp;&nbsp;

Note:
- There are **several edge-cases** that are currently being ironed out! 
- If something stops working, try restarting the dashboard and navigating to that page from fresh
- Make sure to **check the outputs of cmd** (helpful debugging info that might not be shown on the Dash)
- BLAZE has been developed and tested on Python 3.9 (Python 3.11 and above don't support a few libraries) 


&nbsp;&nbsp;

## Install using Docker: Local Development

Install Docker and Docker Composer following the instructions on the link `https://docs.docker.com/engine/install/`

Run below command to build and run the environment
`docker compose up -d`

## Using the Conversational AI

### Installation

With `blaze/conv` as the working directory, proceed with the following steps.

Create a virtual environment with Python 3.8.10

```
python3.8 -m venv .venv
source .venv/bin/activate
```

Install requirements in a virtual environment with 

`pip install -r requirements.txt`

Build the application with

`python -m conv build`

(This step may take about 15 minutes wihtout a GPU)

And run in the commandline with

`python -m conv converse`


### Sources for training data
- greet: food_ordering/greet/train.txt
- exit: food_ordering/exit/train.txt
- ask_question: manual data entry + mindmeld data augmentation
- get_summary: manual data entry + mindmeld data augmentation
- upload_data: manual data entry + mindmeld data augmentation



## Instructions to install and run Supported Models, Knowledge Bases

Installation of different models and knowledge bases is optional, depending on the needs of the user. Each must be installed
and ran according to their own instructions in order to be used by BLAZE.

Following are examples to install and run `Elasticsearch` and `ColBERT`.

***Installing Elasticsearch***

Navigate to [Elasticsearch Installation](https://www.elastic.co/downloads/past-releases/elasticsearch-7-0-0) and 
follow the instructions according to your specific setup. 

> NOTE: BLAZE does **not currently support** Elasticsearch 8 or higher! 

In order to launch elasticsearch, open a new terminal, navigate to the elasticsearch directory, and run either of the following: 
- `./bin/elasticsearch` (Linux/Mac)
- `.\bin\elasticsearch.bat` (Windows)

Now, leave this terminal window open! 

&nbsp;&nbsp;

***Installing ColBERT***

Clone the [ColBERT repository](https://github.com/stanford-futuredata/ColBERT/tree/new_api) in the `blaze` root directory. 

> NOTE: There might be some issues with environments, these will be resolved by next commit! 

Once downloading the ColBERT files, make sure to uncomment the three lines near the top 
of the file `ColBERTSearch.py`. More instructions are detailed at the top of this file. 

After this, navigate to the `get_sidebar()` function in `app_elements.py` and make sure to 
toggle the "Disabled" option next to ColBERT. You should be good to go now! 

&nbsp;&nbsp;

***Installing Knowledge Graph***

Stay tuned, support for this is coming soon! 

&nbsp;&nbsp;


## Get in touch

If you would like to contact the team, please feel free to email us at **blaze-github-owners@cisco.com**.

For bugs or other issues, you can also use the **Issues** section of the repository.

Finally, for broader topics around the project, you may also use the **Discussions** section.
