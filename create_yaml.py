import yaml

data = {
    'Function': 'Search',
    'benchmarking': False,
    'comparing': False,
    'model': {
        'name': "ColBERT",
        'title': "ColBERT - Scalable BERT-Based Search",
        'l_info': "https://arxiv.org/abs/2004.12832",
        'l_repo': "https://github.com/stanford-futuredata/ColBERT"
    },
    'data': {
        "DATA_PATH": "./data/squad2_data",
        "FILES_PATH": "./data/user_files",
        "DATA_SETS": "1",  # Use * for all Squad Datasets,
        "DEFAULT": "1973_oil_crisis"
    },
    'states': {
        'has_input_file': False,
        'has_indexed': False,
        'chosen_name': None,
        'chosen_path': None,
        'm_in_use': 1,
        'q_placeholder': "Once the input has been indexed, ask away...",
        'a_placeholder': "... and the output will be shown here!"
    },
    'metrics': {
        'latency': [-1, -1, -1],
        'search_avg': -1,
        'num_GPUs': 1,
        'accuracy': [-1, -1]
    },

}


with open("trial_inp.yaml", mode="wt", encoding="utf-8") as file:
    yaml.dump(data, file)
