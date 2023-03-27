## Conversational AI for use with ASKI

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
