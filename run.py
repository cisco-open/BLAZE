import argparse
from time import sleep
import yaml
<<<<<<< HEAD
#from aski.dash_files.app_callbacks import *
from aski.flask_servers.app import *
from multiprocessing import Process
import os
import subprocess


def run_app_server(app, port=3000, ip='localhost'):
   # os.environ["WERKZEUG_RUN_MAIN"] = 'true'
    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    app.run(host=ip, port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file',
                        help='YAML file that describes the NLP pipeline',
                        )
    args = parser.parse_args()

    with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)
   # print(data)
   # p = Process(target=run_app, args=(data,))
    with open("tmp.yaml", mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file)
    print("Created tmp.yaml")
    sleep(5)
    app = create_app(data)
    p1 = Process(target=run_app_server, args=(app,))
    # p.start()
    p1.start()
    # p.start()
    subprocess.Popen(['python', 'run_dash.py', 'tmp.yaml'])
    p1.join()
    # p.join()

    # os.remove("tmp.yaml")
=======
from aski.dash_files.app_callbacks import run_app 
from aski.datasets.squad import Squad
from aski.datasets.cnn_dailymail import CNNDailyMail
from datasets import get_dataset_config_names

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
>>>>>>> abstraction
