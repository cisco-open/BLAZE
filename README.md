# BLAZE - Building Language Applications Easily 🔥

&nbsp;&nbsp;

> ***tl;dr*** - Cisco Research proudly presents BLAZE, a **flexible, standardized, no-code, open-source platform** to easily *assemble, modify, and deploy* various NLP models, datasets, and components

> Check out our [TechBlog](https://techblog.cisco.com/) and [Homepage](https://research.cisco.com/research-projects/blaze) for more information and exciting applications!

> Make sure to use the **Table of Contents** (the three horizontal lines next to README.md) for easier viewing!

&nbsp;&nbsp;

## What is BLAZE? 

BLAZE is designed to **streamline the integration of Natural Language Pipelines into software solutions**[^1]. We offer an open, extensible framework to benchmark existing solutions and compare them with novel ones.

[^1]: Check out our first [TechBlog](https://techblog.cisco.com/) to learn more about BLAZE's background! 

The building blocks of BLAZE are **flexible blocks of the NLP pipeline**. The functionality of different stages in the pipeline are abstracted out to create *blocks that can be combined in various ways*. Users can arrange these Lego-like blocks to create new recipes of varying NLP pipelines. 

In such, BLAZE will help democratize NLP applications, providing a no-code solution to experiment with SOTA research and serving as a framework to implement NLP pipeline recipes into usable solutions. 


&nbsp;&nbsp;

## Current Features

BLAZE currently supports the following building blocks and sample applications: 

| **Data(sets)** | SQUAD 2.0, BillSum, XSum, CNN Dailymail, HuggingFace* |
|:--------------:|:-----------------------------------------------------:|
|  **User Data** | TXT files, WebEx Transcripts (Live, Pre-Recorded)     |
| **Processing** |         *Enterprise LLM Gateway, coming soon!*        |
|   **Models**   |   GPT-3 Variants, ColBERT, ElasticBERT, HuggingFace*  |
| **Metrics**    |   BertScore, Bleu, Rouge, Accuracy, Latency           |
| **Interfaces** | React App, Dash App, WebEx Bot, WebEx Plugin, POSTMAN |

> HF* - BLAZE's flexible design enables seamless integration of new components, many of which are underway! 

&nbsp;&nbsp;

In addition, we have several sample applications, each of which are detailed below: 

1. **Semantic Search on User-Uploaded Documents** - [TechBlog: Building WebApps with BLAZE](https://techblog.cisco.com/)
2. **Benchmarking ElasticBERT Q/A on SQUAD 2.0** - [TechBlog: Building WebApps with BLAZE](https://techblog.cisco.com/)
3. **Transcript Analysis with WebEx ChatBot** - [TechBLog: Building ChatBot with BLAZE](https://techblog.cisco.com/)
4. **Embedded WebEx Meeting Assistant Plugin** - [TechBlog: Building Plugins with BLAZE](https://techblog.cisco.com/)


&nbsp;&nbsp;

Some of our more-specific offerings include: 

| Feature | Sample | 
| ----------------|:---------------:|
| **(Tool) Drag-and-Drop Builder** <ul><li>Visual builder for configuring and deploying pipelines</li><li>Allows for building from scratch or uploading existing pipelines (visualize "recipes")</li><li>Converts recipe into downloadable YAML config file</li><li>Generates and launches custom NLP pipeline solution</li></ul> | ![Builder](./docs/images/drag-and-drop-best-big-gif.gif) | 
| **(Interface) Dashboard WebApp** <ul><li>Visual representation of generated pipeline</li><li>Supports semantic search, summarization, file upload, etc.</ul> |  ![Custom](./docs/images/custom_qna.PNG "Custom Q/A") | 
| **(Interface) Conversational AI** <ul><li>Interact with generated pipeline through natural language</li><li>Can be purely functional or conversational</li><li>Powered by Cisco MindMeld</li></ul>| ![ChatBot](./docs/images/Slide16.jpg) |
| **(Function) Model Benchmarking** <ul><li>Benchmark selected model on select knowledge base(s)</li><li>Gives metrics such as latency, accuracy (real-time graphs)</li><li>Displays incorrect questions and trends in performance</li></ul>| ![Benchmark](./docs/images/better-benchmark-gif.gif)|
| **(Function) Model Comparison** <ul><li>Benchmark multiple models on selected knowledge base(s)</li><li>Gives metrics such as latency, accuracy (real-time graphs)</li><li>Compares trends in performance (ex. areas of strength)</li></ul>| ![Comparison](./docs/images/model_comparison.png)|



&nbsp;&nbsp;

## Usage - As Easy as 1, 2, 3

The BLAZE framework operates in three stages: **Build**, **Execute**, and **Interact**

### Build 

In the Build stage, users can **specify the models, data, and processing components** of their pipeline using a YAML format. THey can create a fresh *recipe* via a block-based drag-and-drop UI, modify a pre-existing recipe, or use one directly out of the box. The YAML file contains the specifications of their custom pipeline. 

> Our drag-and-drop builder tool allows one to create, visualize, upload, and download YAML recipes. 

Upon completing the drag-and-drop step, users can examine their generated YAML recipes. For example, here we can examine what the generated YAML recipe looks like for a virtual meeting assistant. 

[YamlExample](./docs/images/YAML_Example.PNG)

> We provide several pre-made YAML files recipes in the `yaml` folder as well! 

&nbsp;&nbsp;

### Execute 

In the Execute stage, BLAZE utilizes the YAML file generated or chosen in the preceding stage to **establish a server, hosting the appropriate models, datasets, and components as specified**. This server servers as the heart of the pipeline, allowing users to *interact with their specified configuration of components* to run their task. 

The following diagram represnts the architecture, illustrating how the server enables pipeline functionality. 

[Architecture](./docs/images/Architecture.PNG)

> YAML files can be executed via the `run.py` script, which is discussed in **Installation** below! 

&nbsp;&nbsp;

### Interact 

In the Interact stage, users can choose to interact with their hosted, active pipelines through a number of pre-build interfaces, or directly access each functionality through REST API services. Our current offering of interfaces include: 

* WebApps (both in React and Dash)
* ChatBots (powered by WebEx, MindMeld)
* Plugins (both WebEx bots and WebEx Meeting Apps)
* Postman (or any other REST API Client)

All of these interfaces are ***automatically generated*** and are **specific** to the **user's pipeline**. 

> Steps to launch each of the above interfaces are discussed in the **Installation** below!

Powered by BLAZE's modular design, these varying interfaces were made **without a single line of code**. All a user has to do is *specify their task* in either the drag-and-drop builder or in the YAML recipe directly. 


&nbsp;&nbsp;

## Installation 


&nbsp;&nbsp;

BLAZE is currently supported on **Linux**, **Windows**, and **Mac**. Specific instrucutions shown below: 

### **1. Environment Setup (Python, Pip)**

At the very start, please clone this repostiory using 
    `git clone https://github.com/cisco-open/Blaze.git`

Next, we must install the necessary packages for BLAZE. 

#### Option 1 - Pyenv: Local Development

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

Finally,install packages and modules using 
`pip install -r requirements.txt`


&nbsp;&nbsp;

#### Option 2 - Install using conda: Local development 

> NOTE: The use of Conda may require the use of Anaconda Commercial Edition to comply with Anaconda's Terms of Service if your use is considered commercial according to Anaconda. More information about Anaconda's Terms of Service and what qualifies as commercial usage can be found here: https://www.anaconda.com/blog/anaconda-commercial-edition-faq/ 

Create your conda environment with

conda env create -f aski_env.yml

Then, activate your conda environment with

conda activate aski

&nbsp;&nbsp;


### **2. (Build) Drag-and-Drop YAML Builder** 


Run the Program with:
`python build.py`

&nbsp;&nbsp;

### **3. (Execute) Running a Pipeline**

Now, a link should appear (ex. `Dash is running on http://127.0.0.1:5000/`). Run this link in your browser to open the dashboard!

`python run.py yaml/<file-name>.yaml`

&nbsp;&nbsp;

### **4. (Interact) Checking POSTMAN** 

&nbsp;&nbsp;

### **5. (Interact) Launching WebApps** 

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

### **6. (Interact) WebEx Integrations** 

### **7. (Interact) Conversational AI** 

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


> Please raise an issue or reach out to our mailing list ([blaze-github-owners@cisco.com](blaze-github-owners@cisco.com)) with any questions!

## Acknowledgements 

Thank you so much for checking us out! 




***Installing Elasticsearch***

Navigate to [Elasticsearch Installation](https://www.elastic.co/downloads/past-releases/elasticsearch-7-0-0) and 
follow the instructions according to your specific setup. 

> NOTE: ASKI does **not currently support** Elasticsearch 8 or higher! 

In order to launch elasticsearch, open a new terminal, navigate to the elasticsearch directory, and run either of the following: 

place the elastic folder as same hirerachy as ASKI project folder to start elastic service when running run.py file insted of running it manually using the commands below

- `./bin/elasticsearch` (Linux/Mac)
- `.\bin\elasticsearch.bat` (Windows)

Now, leave this terminal window open! 



> [BLAZE Drag-and-Drop - README](drag/README.md) | [BLAZE Conversational AI - README](conv/README.md)


&nbsp;&nbsp;
