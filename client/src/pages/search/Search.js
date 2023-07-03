import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import searchStyles from "./Search.module.css";
import { setConfig } from "../../slice/configLoadSlice";
import { listFiles } from "../../slice/datasetSlice";
import { FileSelectComponent } from "../../components/fileSelect";
import { ModelSelect } from "../../components/modelSelect";
import { DatasetSelect } from "../../components/datasetSelect";
import axios from "axios";
import { Sidebar } from "../../layouts/Sidebar";
import { Layout } from "../../layouts/Layout";

const baseURL = "http://localhost:3000/";

export function SearchPage(props) {
  const dispatch = useDispatch();

  const config = useSelector((state) => state.config.config);
  const fileList = useSelector((state) => state.dataset.listFiles);
  const selectedFile = useSelector((state) => state.dataset.selectedFile);
  const selectedFileDetails = useSelector(
    (state) => state.dataset.selectedFileDetails
  );
  const modelState = useSelector((state) => state.models);
  const datasetState = useSelector((state) => state.dataset);
  const [answer, setAnswer] = useState("...output will be shown here");
  const [input, setInput] = useState("");

  if (config == null) {
    return <></>;
  }
  const handleInitilize = (e) => {
    console.log(selectedFileDetails);
    if (modelState.selectedModel !== null && selectedFileDetails !== null) {
      setAnswer("Initilizing");
      axios
        .post(baseURL + "models/model/initialize", {
          model: modelState.selectedModel,
          filename: selectedFile.filename,
          filecontent: selectedFileDetails.content,
        })
        .then((response) => {
          console.log(response.data);
          setAnswer(response.data.response);
        });
    } else {
      alert("Input error");
    }
  };
  const handleAskQuestion = (e) => {
    console.log(selectedFileDetails);
    if (modelState.selectedModel !== null && selectedFileDetails !== null) {
      setAnswer("Processing");
      axios
        .post(baseURL + "search", {
          model: modelState.selectedModel,
          query: input,
        })
        .then((response) => {
          setAnswer(response.data.result[0].res);
        });
    }
  };

  return (
    <>
      <Sidebar>
        <ModelSelect config={config} />
        <DatasetSelect config={config} />
      </Sidebar>
      <div className={searchStyles.bdivider} />
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
          <div className={searchStyles.bg343a40 + " w-50 p-3 m-3"}>
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

          <div className={searchStyles.bg343a40 + " w-50 p-3 m-3 text-center"}>
            <h5 className="text-center">Question-Answering</h5>
            <br></br>
            <div className="form-group">
              <input
                type="text"
                className="form-control"
                id="question"
                placeholder="Once the input has been indexed, ask away..."
                onInput={(e) => setInput(e.target.value)}
              />
              <button
                type="button"
                className="btn btn-primary m-3"
                onClick={(e) => handleAskQuestion(e)}
              >
                Ask Q
              </button>
              <button
                type="button"
                className="btn btn-secondary m-3"
                onClick={(e) => handleInitilize(e)}
              >
                Index
              </button>
            </div>

            <br></br>

            <div className="bg-dark-subtle card height-30 overflow-scroll p-2">
              {answer}
            </div>
            <br></br>
          </div>
        </div>
      </Layout>
    </>
  );
}
