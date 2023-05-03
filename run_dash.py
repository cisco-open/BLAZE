
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


"""
====================================================
Run Dash
====================================================
This file can be run to only start the Dashboard. 

"""

import argparse
import yaml

from aski.dash_files.app_callbacks import run_app


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_file',
                        help='YAML file that describes the NLP pipeline',
                        )
    parser.add_argument('-p', type=int, default=5001,
                        required=False, help="defines port ot be used")
    args = parser.parse_args()

    with open(args.yaml_file, mode="rt", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    print(f"\n==== Starting Flexible NLP Pipeline ===\n")
    print(f"(run) > Loaded data from yaml: {data}\n")
    print(f"(run) > Starting dashboard...")

    port = args.p
    run_app(data, port)


if __name__ == "__main__":
    main()
