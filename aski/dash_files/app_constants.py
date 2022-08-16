"""

This file stores all constants utilized by the ASKI Dashboard. 
If a certain style, color, or image is utilized multiple times 
throughout the dashboard (ex. Cisco's Logo, Fonts, Styles), it 
is added here for easier management and more readable code. 

This file is broken down into the following sections: 

    Content Stylings (Python dicts)
    Colors (hex, some w/ transparency)
    Defaults (Paths, Toggles, Texts)
    Media (Fonts, Images, Links)

"""


# === Content Stylings === #

CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem 2rem 1rem",
    "background-color": "#222222",
    'font': {'family': 'Quicksand'},
    "overflow": "scroll",
    "height" : "60rem"
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#424242",
    "overflow": "scroll"
}


# === Colors (hex) === #

WHITE = "#FFFFFF"
CREAM = "#FFE5B4"
BLACK = "#000000"
TEAL = "#049FD9"

CONST_RESULTS = {
                    "m_name": "",
                    "f_name": "",
                    "root": "",
                    "questions": {
                        "num_qf": 0,
                        "num_qs": 0,
                        "all_qs": [],
                        "tot_qs": 0,
                    },
                    "times": {
                        "avg_ts": 0,
                        "all_ts": [],
                    },
                    "metrics": {
                        "correct_arr": [],
                        "incorrect_d": {},
                        "accuracy_num": 0,
                        "accuracy_prc": 0,
                    }
                }

SEARCH_BOX_PLACEHOLDER = "Once the input has been indexed, ask away..."
ANSWER_BOX_PLACEHOLDER = "... and the output will be shown here!"

# === Defaults (Paths, Toggles) === #

#SQUAD_DATA_PATH = "./data/squad2_data"
#FILES_DATA_PATH = "./data/user_files"

# SQUAD_DATA_SETS = "1" # Use * for all Squad Datasets
#SQUAD_DEFAULT = "1973_oil_crisis"

SIDEBAR_TEXT = "A Comparison of Semantic Search Implementations"
PARAMS_PATH = "aski/params/data_dict.txt"
USER_FILES_PATH = "data/user_files"

# === Fonts, Images, Links === #

FONT_QUICKSAND = "https://fonts.googleapis.com/css?family=Quicksand&display=swap"
FONT_QUICKSAND = "https://fonts.googleapis.com/css?family=Quicksand&display=swap"

CISCO_LINK = "https://research.cisco.com/"
CISCO_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Cisco_logo_blue_2016.svg/2560px-Cisco_logo_blue_2016.svg.png"

DATA_PATH  = './data/squad'
FILES_PATH = './data/user_files'
DATA_SETS  = '1'
DEFAULT    = '1973_oil_crisis'
