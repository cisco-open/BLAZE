import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import summarizationStyles from "./Summarization.module.css";
import { setConfig } from "../../slice/configLoadSlice";
import { listFiles } from "../../slice/datasetSlice";
import { FileSelectComponent } from "../../components/fileSelect";
import { ModelSelect } from "../../components/modelSelect";
import { DatasetSelect } from "../../components/datasetSelect";
import axios from "axios";
import { Sidebar } from "../../layouts/Sidebar";
import { Layout } from "../../layouts/Layout";

const baseURL = "http://localhost:3000/";

export function SummarizationPage(props) {
  // Declare a new state variable, which we'll call "count"
  const dispatch = useDispatch();

  const config = useSelector((state) => state.config.config);
  const fileList = useSelector((state) => state.dataset.listFiles);
  const selectedFileDetails = useSelector(
    (state) => state.dataset.selectedFileDetails
  );
  const modelState = useSelector((state) => state.models);
  const datasetState = useSelector((state) => state.dataset);
  const [summary, setSummary] = useState("...output will be shown here");

  if (config == null) {
    return <></>;
  }

  
  const benchmark = config["function"]["benchmarking"];
  const custom = config["function"]["custom"];
  const comparing = config["function"]["comparing"];

  const handleSummarize = (e) => {
    console.log(modelState.selectedModel);
    if (modelState.selectedModel !== null && selectedFileDetails !== null) {
      setSummary("Processing");
      axios
        .post(baseURL+"summary", {
          model: modelState.selectedModel,
          function:"summarize_text",
          content: selectedFileDetails.content,
        })
        .then((response) => {
          console.log(response)
          setSummary(response.data.result[0]);
        });
    }
  };

  return (
    <>
      <Sidebar>
        <ModelSelect config={config} />
        <DatasetSelect config={config} />
      </Sidebar>
      <div className={summarizationStyles.bdivider} />
      <Layout>
        <center>
          <br></br>
          <button
            className="btn btn-outline-info"
            style={{
              fontFamily: "Quicksand",
              fontSize: 40,
              padding: "1rem",
              marginBottom: "2rem",
            }}
          >
            BLAZE Dashboard - Cisco Research
          </button>
        </center>
        <div className="d-flex text-white">
          <div className={summarizationStyles.bg343a40 + " w-50 p-3 m-3"}>
            <center>
              <h5>Input Text(s)</h5>
            </center>
            <div className="row">
              <div className="col">Please choose the file</div>
              <div className="col">
                <FileSelectComponent datasets={config["datasets"]} />
              </div>
            </div>
            <br></br>
            <div className="bg-dark-subtle card height-30 overflow-scroll p-2">
              {selectedFileDetails && selectedFileDetails.content}
            </div>
          </div>

          <div
            className={
              summarizationStyles.bg343a40 + " w-50 p-3 m-3 text-center"
            }
          >
            <h5 className="text-center">Summarization</h5>
            <br></br>
            <br></br>

            <div className="bg-dark-subtle card height-30 overflow-scroll p-2">
              {summary}
            </div>
            <br></br>
            <center>
              <button
                id="custom-begin-summarization"
                className="btn btn-outline-info"
                style={{ fontSize: 26, fontFamily: "Quicksand" }}
                onClick={(e) => handleSummarize(e)}
              >
                Summarize
              </button>
            </center>
          </div>
        </div>
      </Layout>
    </>
  );
}
