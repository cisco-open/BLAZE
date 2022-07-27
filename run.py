import argparse
import yaml
from dash_files.app_callbacks import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file',
        help='YAML file that describes the NLP pipeline',
        )
    args = parser.parse_args()
    
    with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    print(data)
    run_app(data)
