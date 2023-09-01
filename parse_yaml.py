import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('yaml_file',
                        help='YAML file that describes the NLP pipeline',
                        )
parser.add_argument('key', default=None, help="key to retrive")

args = parser.parse_args()

with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
    data = yaml.safe_load(file)

print(data.get(args.key,None))
