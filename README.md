# BLAZE - Building Language Applications Easily 🔥

&nbsp;&nbsp;

> ***tl;dr*** - Cisco Research proudly presents BLAZE, a **flexible, standardized, no-code, open-source platform** to easily *assemble, modify, and deploy* various NLP models, datasets, and components

> Check out our [TechBlog](https://techblog.cisco.com/) and [Homepage](https://research.cisco.com/research-projects/blaze) for more information and exciting applications!

&nbsp;&nbsp;

## What is BLAZE? 

BLAZE is designed to **streamline the integration of Natural Language Pipelines into software solutions**[^1]. We offer an open, extensible framework to benchmark existing solutions and compare them with novel ones before a production shift. 

[^1]: Check out our first [TechBlog](https://techblog.cisco.com/) to learn more about BLAZE's background! 

The building blocks of BLAZE are **flexible blocks of the NLP pipeline**. The functionality of different stages in the pipeline are abstracted out to create *flexible, Lego-like blocks that can be combined in various ways*. Users can add and arrange these building blocks to create new recipes of varying NLP pipelines. In such, BLAZE will help democratize NLP applications, providing a no-code solution to experiment with SOTA research and serving as a framework to implement NLP pipeline recipes into usable solutions. 


&nbsp;&nbsp;

## Current Features

BLAZE currently supports the following building blocks and sample applications: 

| **Data(sets)** | SQUAD 2.0, BillSum, XSum, CNN Dailymail, HuggingFace* |
|:--------------:|:-----------------------------------------------------:|
|  **User Data** | TXT files, WebEx Transcripts (Live, Pre-Recorded)     |
| **Processing** |         *Enterprise LLM Gateway, coming soon!*        |
|   **Models**   |   GPT-3 Variants, ColBERT, ElasticBERT, HuggingFace*  |
| **Interfaces** | React App, Dash App, WebEx Bot, WebEx Plugin, POSTMAN |

> Huggingface\* - BLAZE's flexible design enables seamless integration of new components, many of which are underway! 

&nbsp;&nbsp;

In addition, we have several sample applications, each of which are detailed below: 

1. **Semantic Search on User-Uploaded Documents** - [TechBlog: Building WebApps with BLAZE](https://techblog.cisco.com/)
2. **Benchmarking ElasticBERT Q/A on SQUAD 2.0** - [TechBlog: Building WebApps with BLAZE](https://techblog.cisco.com/)
3. **Transcript Analysis with WebEx ChatBot** - [TechBLog: Building ChatBot with BLAZE](https://techblog.cisco.com/)
4. **Embedded WebEx Meeting Assistant Plugin** - [TechBlog: Building Plugins with BLAZE](https://techblog.cisco.com/)


&nbsp;&nbsp;

Some of our more-specific offerings include: 

- **Drag-and-Drop Pipeline Builder** 
  - Visual builder for configuring and deploying pipelines
  - Allows for building from scratch (adding, connecting components)
  - Allows for uploading existing pipelines (visualize "recipes") 
  - Converts custom recipe into downloadable YAML config file 
  - Generates and launches custom NLP pipeline solution

<!-- <ul><li>item1</li><li>item2</li></ul> --> 

 ![Custom](./docs/images/custom_qna.PNG "Custom Q/A")
![Comparison](./docs/images/model_comparison.png)





- **Conversational AI (Webex Bot)** 
  - Interface with BLAZE to specify pipeline components
  - Generate and launch custom NLP pipeline solution 

- **Visual Dashboard Web App** 
  - Visual representation of generated pipeline
  - Supports semantic search, summarization, file upload, etc. 

- **Conversational AI (Webex Bot)** 
  - Interact with generated pipeline through natural language
  - Can choose knowledge base (ex. upload file, view all files) 
  - Can index model and retrieve results (ex. summarize this doc) 
  - Can retrieve knowledge base, model, and metrics info 

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

## Usage - As Easy as 1, 2, 3

The BLAZE framework operates in three stages: **Build**, **Execute**, and **Interact**

### Build 



### Execute 

### Interact 



&nbsp;&nbsp;

## Installation 


&nbsp;&nbsp;

## Install using Pyenv: Local Development

Install Dependencies
For Ubuntu/Debian
`sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl`

For Fedora/CentOS
`sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel`

Install Pyenv
`curl https://pyenv.run | bash`

Install Python version 3.9.16 using below command
`pyenv install -v 3.9.16`

check python version installed in pyenv using command
`pyenv versions`

Create virtual environment with specific version using below command
`pyenv virtualenv 3.9.16 venv`

Activate virtual environment using 
`pyenv local venv` or `pyenv activate <environment_name>`

You can verify this by running the following:
`pyenv which python`

Install packages and modules using 
`pip install -r requirements.txt`

Run the Program with:
`python build.py`

Now, a link should appear (ex. `Dash is running on http://127.0.0.1:5000/`). Run this link in your browser to open the dashboard!

`python run.py yaml/<file-name>.yaml`


## To run React Frontend
Install node in Windows/Mac/Linux
Goto https://nodejs.org/en/download/ install nodejs and npm, check installation with
`node -v and npm -v`

Goto /client dir using
`cd client`

Install node_modules using command 
`npm install`

Run Frontend with 
`npm start`

## To run dash Frontend
`python run_fr.py yaml/<file-name>.yaml`


&nbsp;&nbsp;

## Install using conda: Local development 

## NOTE: The use of Conda may require the use of Anaconda Commercial Edition to comply with Anaconda's Terms of Service if your use is considered commercial according to Anaconda. More information about Anaconda's Terms of Service and what qualifies as commercial usage can be found here: https://www.anaconda.com/blog/anaconda-commercial-edition-faq/ 

Create your conda environment with

conda env create -f aski_env.yml

Then, activate your conda environment with

conda activate aski

## Using the Conversational AI

Build the conversational model with

`python -m conv build`

(This step may take about 15 minutes without a GPU)

And run the AI in the command line with

`python -m conv converse`

To run the webex bot server, start an ngrok tunnel with

`ngrok http 8080 --region=eu`

It is important that the region is *not* 'us'.

Set the environment variables BOT_ACCESS_TOKEN (received when you register your bot) and WEBHOOK_URL (generated by ngrok) and change to the conv directory. Then run

`python webex_bot_server.py`

***Sources for training data***
- greet: food_ordering/greet/train.txt
- exit: food_ordering/exit/train.txt
- ask_question: manual data entry + mindmeld data augmentation
- get_summary: manual data entry + mindmeld data augmentation
- upload_data: manual data entry + mindmeld data augmentation


## Supported Models, Knowledge Bases

***Installing Elasticsearch***

Navigate to [Elasticsearch Installation](https://www.elastic.co/downloads/past-releases/elasticsearch-7-0-0) and 
follow the instructions according to your specific setup. 

> NOTE: ASKI does **not currently support** Elasticsearch 8 or higher! 

In order to launch elasticsearch, open a new terminal, navigate to the elasticsearch directory, and run either of the following: 

place the elastic folder as same hirerachy as ASKI project folder to start elastic service when running run.py file insted of running it manually using the commands below

- `./bin/elasticsearch` (Linux/Mac)
- `.\bin\elasticsearch.bat` (Windows)

Now, leave this terminal window open! 

&nbsp;&nbsp;


> [BLAZE Drag-and-Drop - README](drag/README.md) | [BLAZE Conversational AI - README](conv/README.md)


&nbsp;&nbsp;
