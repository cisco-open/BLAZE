from dash import Dash, html, dcc, Input, Output, State


def get_search_callbacks(app, page, params): 

    # === Callback for Custom Question/Answering page === #

    @app.callback(Output("custom-content", "children"),
                  [Input("search-custom-choose-file", "value"),
                   Input("search-custom-begin-index", "n_clicks"), 
                   Input("search-custom-ask-q-button", "n_clicks")],
                  [ State("search-custom-enter-q-box", "value")])

    def render_custom_content(file_chosen, index_button, ask_button, query_text):

        ### Component 01 - Selecting User File ###

        if file_chosen:

            params._data_dict['states']['has_input_file'] = True 

            if (file_chosen.split("/")[-1] == "story.txt"):
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-2]).replace("_", " ")
            else:
                params._data_dict['states']['chosen_path'] = (
                    file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen



        ### Component 02 - Indexing (Init) ###

        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            f_name = params._data_dict['states']['chosen_data']

            f = open(params._data_dict['states']['chosen_path'], "r")
            lines = f.readlines()[1:]
            f.close()
            f_content = "".join(lines)

            print(f"(callback_search) > Begun indexing {params._data_dict['states']['model_active']}")
            
            params._data_dict['states']['model_objs'][0].load_model(f_name, f_content)
            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")
        


        ### Component 03 - Clicking "Ask Q" ###

        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > About to ask: {query_text}")

            res, time = params._data_dict['states']['model_objs'][0].file_search(query_text)
            ans = "Unable to find an answer."

            try:
                ans = res[0]['res'] + f" ({round(time, 2)}s)"
                print(res[0])
            except:
                pass

            print(f"(callback_search) > Received answer: {ans}")

            params._data_dict['states']['query'] = query_text
            params._data_dict['states']['result'] = ans


        return page.get_page_custom(params)




    # === (03) Callback for Solo Benchmarking page === #

    @app.callback(Output("squad-content", "children"),
                  [Input("squad-file", "value"),
                   Input("squad-begin-index", "n_clicks")],
                  [])
    def render_squad_content(s_chosen, s_bench_button):
        print("Now, we're in this callback func")
        results = None

        if s_chosen:
            data['squad']['has_input_file'] = True

            if (s_chosen.split("/")[-1] == "story.txt"):
                data['squad']['chosen_name'] = (
                    s_chosen.split("/")[-2]).replace("_", " ")
            else:
                data['squad']['chosen_name'] = (
                    s_chosen.split("/")[-1]).replace("_", " ")

            data['squad']['chosen_path'] = s_chosen

            print(s_chosen)

        if s_bench_button == 1 and data['squad']['has_input_file'] and not data['squad']['has_indexed']:

            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            p1 = multiprocessing.Process(target=squad_benchmark, args=(
                pQueue, data['squad']['chosen_name'], data['squad']['chosen_path']))
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
                  [Input("compare-squad-file", "value"),
                   Input("compare-begin-index", "n_clicks")],
                  [])
    def render_compare_content(s_chosen, s_bench_button):
        print("Now, we're in this callback func")
        results = None

        if s_chosen:
            data['squad']['has_input_file'] = True

            if (s_chosen.split("/")[-1] == "story.txt"):
                data['squad']['chosen_name'] = (
                    s_chosen.split("/")[-2]).replace("_", " ")
            else:
                data['squad']['chosen_name'] = (
                    s_chosen.split("/")[-1]).replace("_", " ")

            data['squad']['chosen_path'] = s_chosen

            print(s_chosen)

        if s_bench_button == 1 and data['squad']['has_input_file'] and not data['squad']['has_indexed']:

            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            p1 = multiprocessing.Process(target=squad_benchmark, args=(
                pQueue0, data['squad']['chosen_name'], data['squad']['chosen_path'], "ColBERT"))
            p2 = multiprocessing.Process(target=squad_benchmark, args=(
                pQueue1, data['squad']['chosen_name'], data['squad']['chosen_path'], "Elastic"))

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
