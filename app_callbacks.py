"""

This file is what starts the ASKI Dashboard! In order to run, simply: 

- Create your conda environment with "conda env create -f aski_env.yml" 
- Activate your conda environment with "conda activate aski-benchmark" 
- Run this file with "python app_callbacks.py" and a link should appear! 


This file contains ten callbacks, which are what make the Dashboard 
dymanic. All callbacks (as well as their descriptions) are listed below: 

    determine_which_page(m_chosen, b_chosen, f_contents, f_name) - high-level, which page 
    render_custom_content(m_chosen, b_chosen, f_contents, f_chosen, i_button, q_button, f_name, q_text) - only callback for custom Q/A

    render_squad_content(s_chosen, s_bench_button) - for solo benchmarking page 
    render_progress_content(n, existing_state) - for updating the progress bar 

    render_compare_content(s_chosen, s_bench_button) - for model comparison page 
    render_compare_progress_content0(n, existing_state) - for starting model0 
    render_compare_progress_content1(n, existing_state) - for starting model1

    render_progress_content(n, existing_state) - update incorrect answers, solo bench
    render_progress_content0(n, existing_state) - update incorrect answers, model0
    render_progress_content1(n, existing_state) - update incorrect answers, model1

"""


from dash import Dash, html, dcc, Input, Output, State 
import dash_bootstrap_components as dbc

from app_constants import * 
from app_elements import * 
from app_helpers import * 

from model_helpers.helpers_benchmark import * 
from ColbertSearch import * 
from ElasticSearch import * 

import os, base64, multiprocessing
from multiprocessing import Queue



def run_app(): 

    # Data is a dictionary used extensively throughout the app
    data = initialize_data() 


    # Definiting our app, its styles, and its layout  
    app = Dash(
        __name__, 
        external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_QUICKSAND], 
    )

    content = html.Div([get_content(data)], id="page-content")

    app.css.config.serve_locally = True
    app.layout = html.Div([dcc.Location(id="url"), get_sidebar(), content])


    pQueue = Queue() # For Solo
    pQueue0 = Queue() # For ColBERT 
    pQueue1 = Queue() # For Elastic

    model = [None] 


    """
    
    The rest of this function is simply defining our 10 callbacks. 
    
    """


    # === (01) Callback for determining which page === #

    @app.callback(Output("page-content", "children"), 
                [Input("input-radioitems-model", "value"), Input("input-switches-data", "value"), Input("input-button-file", "contents")],
                [State("input-button-file", "filename")])
    
    def determine_which_page(m_chosen, b_chosen, f_contents, f_name): 
        
        if data['states']['m_in_use'] != m_chosen: 

            data['states'] =  {
                                'has_input_file' : False, 
                                'has_indexed' : False, 
                                'chosen_name' : None, 
                                'chosen_path' : None, 
                                'm_in_use' : m_chosen,
                                'q_placeholder' : "Once the input has been indexed, ask away...",
                                'a_placeholder' : "... and the output will be shown here!"
                              }

            if m_chosen == 1:

                data['model']['name'] = "ColBERT"
                data['model']['title'] = "ColBERT - Scalable BERT-Based Search"
                data['model']['l_info'] = "https://arxiv.org/abs/2004.12832"
                data['model']['l_repo'] = "https://github.com/stanford-futuredata/ColBERT"

            elif m_chosen == 2:

                data['model']['name'] = "Elastic"
                data['model']['title'] = "Elasticsearch - Distributed Search Engine"
                data['model']['l_info'] = "https://www.elastic.co/"
                data['model']['l_repo'] = "https://elasticsearch-py.readthedocs.io/en/v8.1.2/"

            #m_in_use += m_chosen - m_in_use 


        ### Callback 02 - Uploading User Files ###

        if f_name is not None: 
            content_type, content_string = f_contents.split(',')
            decoded = base64.b64decode(content_string).decode("utf-8") 

            f_path = FILES_DATA_PATH + "/" + f_name

            f = open(f_path, "w")
            f.write(decoded)
            f.close() 

            data['inputs']['n_user'].append(f_name)
            data['inputs']['p_user'].append(f_path) 


        
        print(f"b_chosen {b_chosen}")
        print(f"data_bench {data['benchmarking']}")

        if 2 in b_chosen or data["benchmarking"]: 
            data['benchmarking'] = True 
            return get_benchmark_content(data, pQueue)
    
        if 3 in b_chosen or data["comparing"]: 
            data["comparing"] = True 
            return get_comparison_content(data, pQueue0, pQueue1)

        return get_content(data, pQueue)



    # === (02) Callback for Custom Question/Answering page === #

    @app.callback(Output("custom-content", "children"), 
                [Input("input-radioitems-model", "value"), Input("input-switches-data", "value"), Input("input-button-file", "contents"), Input("input-file", "value"), Input("input-indexing", "n_clicks"), Input("input-qbutton", "n_clicks")], 
                [State("input-button-file", "filename"), State("input-qbox", "value")])

    def render_custom_content(m_chosen, b_chosen, f_contents, f_chosen, i_button, q_button, f_name, q_text):

        ### Callback 03 - Selecting User File ###

        if f_chosen: 

            data['states']['has_input_file'] = True 

            if (f_chosen.split("/")[-1] == "story.txt"):
                data['states']['chosen_name'] = (f_chosen.split("/")[-2]).replace("_", " ")
            else: 
                data['states']['chosen_name'] = (f_chosen.split("/")[-1]).replace("_", " ")

            data['states']['chosen_path'] = f_chosen

 
        ### Callback 04 - Indexing (Init) ###

        if i_button == 1 and data['states']['has_input_file'] and not data['states']['has_indexed']: 

            f_name = data['states']['chosen_name']

            f = open(data['states']['chosen_path'], "r")
            lines = f.readlines()[1:]
            f.close() 
            f_content = "".join(lines) 

            if data['model']['name'] == "ColBERT": 
                print("Begun indexing ColBERT...")
                model[0] = ColbertSearch(f_name, f_content)
            else: 
                print("Begun indexing Elastic...")
                model[0] = ElasticSearch(f_name, f_content)
            
            data['states']['has_indexed'] = True 
            print("Completed indexing...")
            #i_button  += 1


        ### Callback 05 - Clicking "Ask Q" ###

        print(q_button)
        print(data['states']['has_indexed'])

        if q_button == 1 and data['states']['has_indexed']: 

            query = q_text 
            print(q_text)

            res, time = model[0].file_search(query) 

            ans = "Unable to find an answer."

            try: 
                ans = res[0]['res'] + f" ({round(time, 2)}s)"
                print(res[0])
            except: 
                pass 

            print(ans)

            data['states']['q_placeholder'] = query 
            data['states']['a_placeholder'] = ans


        return get_content(data, pQueue) 
    


    # === (03) Callback for Solo Benchmarking page === #

    @app.callback(Output("squad-content", "children"), 
                  [Input("squad-file", "value"),  Input("squad-begin-index", "n_clicks")], 
                  [])
    
    def render_squad_content(s_chosen, s_bench_button): 
        print("Now, we're in this callback func")
        results = None 

        if s_chosen: 
            data['squad']['has_input_file'] = True 

            if (s_chosen.split("/")[-1] == "story.txt"):
                data['squad']['chosen_name'] = (s_chosen.split("/")[-2]).replace("_", " ")
            else: 
                data['squad']['chosen_name'] = (s_chosen.split("/")[-1]).replace("_", " ")

            data['squad']['chosen_path'] = s_chosen

            print(s_chosen)
        
        if s_bench_button == 1 and data['squad']['has_input_file'] and not data['squad']['has_indexed']: 

            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            p1 = multiprocessing.Process(target=squad_benchmark, args=(pQueue, data['squad']['chosen_name'], data['squad']['chosen_path']))
            p1.start() 

            data['squad']['has_indexed'] = True 

            print("NO LONGER IN PROCESS SPAWNING")

        return get_content(data, pQueue)



    # === (04) Callback for updating the progress bar === #

    @app.callback(Output("progress-content", "children"), 
                  [Input('interval-component', 'n_intervals')],
                  [State("progress-content", "children")])
    
    def render_progress_content(n, existing_state): 

        if data['squad']['old_results'] == "DONE": 
            return existing_state

        if data['squad']['has_indexed']: 
            return get_squadMetricsCard(data, pQueue)
        else: 
            return get_spinnyCircle()



    # === (05) Callback for starting indexing of both models (ColBERT, Elastic) === #

    @app.callback(Output("compare-content", "children"), 
                  [Input("compare-squad-file", "value"),  Input("compare-begin-index", "n_clicks")], 
                  [])
    
    def render_compare_content(s_chosen, s_bench_button): 
        print("Now, we're in this callback func")
        results = None 

        if s_chosen: 
            data['squad']['has_input_file'] = True 

            if (s_chosen.split("/")[-1] == "story.txt"):
                data['squad']['chosen_name'] = (s_chosen.split("/")[-2]).replace("_", " ")
            else: 
                data['squad']['chosen_name'] = (s_chosen.split("/")[-1]).replace("_", " ")

            data['squad']['chosen_path'] = s_chosen

            print(s_chosen)
        
        if s_bench_button == 1 and data['squad']['has_input_file'] and not data['squad']['has_indexed']: 

            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            p1 = multiprocessing.Process(target=squad_benchmark, args=(pQueue0, data['squad']['chosen_name'], data['squad']['chosen_path'], "ColBERT"))
            p2 = multiprocessing.Process(target=squad_benchmark, args=(pQueue1, data['squad']['chosen_name'], data['squad']['chosen_path'], "Elastic"))

            p1.start() 
            p2.start()

            data['squad']['has_indexed'] = True 

            print("NO LONGER IN PROCESS SPAWNING")

        return get_content(data, pQueue0, pQueue1)



    # === (06) Callback for determining whether to show Card or Loading (ColBERT) === #

    @app.callback(Output("progress-content0", "children"), 
                  [Input('compare-interval-component', 'n_intervals')],
                  [State("progress-content0", "children")])
    
    def render_compare_progress_content0(n, existing_state): 

        if data['squad']['old_results']["ColBERT"] == "DONE": 
            return existing_state

        if data['squad']['has_indexed']: 
            return get_compareMetricsCard(data, pQueue0, "ColBERT")
        else: 
            return get_compare_spinnyCircle()
    


    # === (07) Callback for determining whether to show Card or Loading (Elastic) === #

    @app.callback(Output("progress-content1", "children"), 
                [Input('compare-interval-component', 'n_intervals')],
                [State("progress-content1", "children")])
    
    def render_compare_progress_content1(n, existing_state): 

        if data['squad']['old_results']["Elastic"] == "DONE": 
            return existing_state

        if data['squad']['has_indexed']: 
            return get_compareMetricsCard(data, pQueue1, "Elastic")
        else: 
            return get_compare_spinnyCircle()


    """

    The following three callbacks are for updating the Incorrect Answers Card. 

    """


    # === (08) Callback for updating Incorrect Answers Card (solo bench) === #

    @app.callback(Output("incorrect-content", "children"), 
                  [Input('interval-component', 'n_intervals')],
                  [State("incorrect-content", "children")])
    
    def render_progress_content(n, existing_state):
        if data['squad']['old_results'] == "DONE": 
            return existing_state

        return get_squadIncorrectCard(data)
   

       # === (09) Callback for updating Incorrect Answers Card (ColBERT) === #

    @app.callback(Output("incorrect-content0", "children"), 
                  [Input('interval-component', 'n_intervals')],
                  [State("incorrect-content0", "children")])
    
    def render_progress_content0(n, existing_state):
        if data['squad']['old_results']["ColBERT"] == "DONE": 
            return existing_state

        return get_compareIncorrectCard(data, "ColBERT")
    

    # === (10) Callback for updating Incorrect Answers Card (Elastic) === #

    @app.callback(Output("incorrect-content1", "children"), 
                  [Input('interval-component', 'n_intervals')],
                  [State("incorrect-content1", "children")])
    
    def render_progress_content1(n, existing_state):
        if data['squad']['old_results']["Elastic"] == "DONE": 
            return existing_state

        return get_compareIncorrectCard(data, "Elastic")




    # Finally, after defining all our callbacks, we can run our app 

    app.config['suppress_callback_exceptions'] = True
    app.run_server(port='5000', debug=True)



if __name__ == "__main__":
    run_app()
