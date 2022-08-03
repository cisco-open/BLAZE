import argparse
import yaml
from aski.dash_files.app_callbacks import run_app 



def main(): 
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

	run_app(data)



if __name__ == "__main__":
	main() 



"""

from aski.models.BartRXF import BartRXF
from aski.datasets.cnn_dailymail import CNNDailyMail
from aski.datasets.squad import Squad
from datasets import get_dataset_config_names

dataset = CNNDailyMail('cnn_dailymail', '3.0.0')

squad = Squad('squad')
dataset._tokenise_dataset('article')

print(dataset._dataset)
print(dataset._tokenized_dataset)

model = BartRXF()

random_example = dataset._get_random_example('article')
print(random_example)

model._summarize_text(random_example)

#model._summarize_dataset(dataset._tokenized_dataset['train'])
"""



