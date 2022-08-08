import argparse
import yaml
from aski.dash_files.app_callbacks import run_app 
from aski.datasets.squad import Squad
from aski.datasets.cnn_dailymail import CNNDailyMail
from datasets import get_dataset_config_names

def main(): 

	configs = get_dataset_config_names("squad")
	print(configs)
	
	dataset = Squad()
	print(dataset._dataset)

	parser = argparse.ArgumentParser()
	parser.add_argument('yaml_file', \
		help='YAML file that describes the NLP pipeline', \
		)
	args = parser.parse_args()
	
	with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
		data = yaml.safe_load(file)

	print(f"\n==== Starting Flexible NLP Pipeline ===\n")
	print(f"(run) > Loaded data from yaml: {data}\n")
	print(f"(run) > Starting dashboard...")

	print(data)

	run_app(data)

if __name__ == "__main__":
	main() 
