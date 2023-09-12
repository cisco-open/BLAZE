import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setConfig } from "../../slice/configLoadSlice";
import { Sidebar } from "./../../layouts/Sidebar";
import { Layout } from "./../../layouts/Layout";
import { ModelSelect } from "../../components/modelSelect";
import { FileSelectComponent } from "../../components/fileSelect";
// import { socket } from "../../socket";
import {CONSTANTS} from "../../CONSTANTS"
import { io } from "socket.io-client";

export function BenchmarkPage() {
  // Declare a new state variable, which we'll call "count"
  const dispatch = useDispatch();

  let serverUrl = CONSTANTS.socketURL;
  let socket = io(serverUrl);

  const [isConnected, setIsConnected] = useState(socket.connected);
  const [benchmark, setBenchmark] = useState({});
  const selectedFile = useSelector((state) => state.dataset.selectedFile);
  const selectedFileDetails = useSelector(
    (state) => state.dataset.selectedFileDetails
  );
  const modelState = useSelector((state) => state.models);


  React.useEffect(() => {
    dispatch(setConfig());
    socket.connect();
    const bencmarkListiner = (message) => {
      console.log("coming here benchmark");
      setBenchmark(message);
    };

    function onConnect() {
      console.log("connected");
      setIsConnected(true);
    }
    socket.on("connect", onConnect);
    socket.on("benchmark", bencmarkListiner);

    return () => {
      socket.off("connect", onConnect);
      socket.off("benchmark", bencmarkListiner);
    };
  }, []);

  const handleClick = (e) => {
    console.log(selectedFileDetails);
    if (modelState.selectedModel !== null && selectedFileDetails !== null) {
      socket.timeout(2000).emit("benchmark", { file: selectedFile.filename }, () => {
        console.log("Emited");
      });
    }
    
  };

  const config = useSelector((state) => state.config.config);
  if (config == null) {
    return <></>;
  }

  return (
    <>
      <div className="row">
        <div className="col-4 py-3">
          <div
            className="row"
            style={{ paddingTop: "1rem", paddingLeft: "1rem" }}
          >
            <div className="col" style={{ color: "white" }}>
              Please choose the file
            </div>
            <div className="col">
              <FileSelectComponent datasets={config["datasets"]} />
            </div>
          </div>
          <center style={{ paddingTop: "2rem" }}>
            <button
              type="button"
              className="btn btn-primary"
              onClick={(e) => handleClick(e)}
            >
              Start Benchmark
            </button>
          </center>

          <center style={{ color: "white", paddingTop: "2rem" }}>
            <div
              className="progress mb-5 mt-5 mx-5"
              style={{ height: "1.5rem", borderRadius: "1rem" }}
            >
              <div
                className="progress-bar progress-bar-striped"
                role="progressbar"
                style={{ width: benchmark.progress + "10%" }}
                aria-valuenow="0"
                aria-valuemin="0"
                aria-valuemax="100"
              >
                {benchmark.progress}
              </div>
            </div>

            <h3>
              Percent Questions Correct: {benchmark.percent_questions_correct}
            </h3>
            <h3>
              Number Questions Correct: {benchmark.number_of_questions_correct}
            </h3>
            <h3>
              Number Questions Total: {benchmark.number_of_questions_total}
            </h3>

            <h3>
              Average Time/Question: {benchmark.average_time_per_question}
            </h3>
          </center>
        </div>

        <div className="col-8">
          <div className="progress m-5">
            <div
              class="progress-bar progress-bar-striped bg-success"
              role="progressbar"
              style={{width: benchmark.percent_questions_correct +"%"}}
              aria-valuenow="0"
              aria-valuemin="0"
              aria-valuemax="100"
            >{benchmark.percent_questions_correct} </div>
          </div>
          <center>
            <h3>All questions answered incorrectly will appear below. </h3>
          </center>
          <div style={{ overflow: "scroll", height: "100vh", padding: "1rem" }}>
            {benchmark.incorrect &&
              benchmark.incorrect.map((data) => {
                return (
                  <div className="card">
                    <div className="card-header">{data.question}</div>
                    <div className="card-body">
                      <p className="card-text">{JSON.stringify(data)}</p>
                    </div>
                  </div>
                );
              })}
          </div>
        </div>
      </div>
    </>
  );
}
