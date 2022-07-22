from dash_files.app_callbacks import *
import yaml

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print('You have specified too many arguments')
        sys.exit()

    if len(sys.argv) < 2:
        print('You need to specify the path to be listed')
        sys.exit()

    yaml_file = sys.argv[1]
    with open(yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    print(data)
    run_app(data)
