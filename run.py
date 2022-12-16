
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0



import argparse
from multiprocessing import Process
import yaml

from aski.dash_files.app_callbacks import run_app
from aski.flask_servers.app import create_app, run_app_server, create_server_config 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file',
                        help='YAML file that describes the NLP pipeline',
                        )
    parser.add_argument('-p', type=int, default=5001, required=False, help="defines port ot be used")

    args = parser.parse_args()

    with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    config = create_server_config(data) 
    app = create_app(data)
    port = args.p

    p_dash = Process(target=run_app, args=(data, port, '0.0.0.0'))
    p_serv = Process(target=run_app_server, args=(app, 3000, '0.0.0.0'))

    p_dash.start()
    
    try: 
        p_serv.start()
        p_serv.join()
    except: 
        print("Flask server may already be running!") 
        
    p_dash.join()
