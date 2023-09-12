import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setConfig } from "../../slice/configLoadSlice";
import { Sidebar } from "./../../layouts/Sidebar";
import { Layout } from "./../../layouts/Layout";
import { ModelSelect } from "../../components/modelSelect";
import { FileSelectComponent } from "../../components/fileSelect";
// import { socket } from "../../socket";

import { io } from "socket.io-client";

export function ComparisionPage() {
  // Declare a new state variable, which we'll call "count"
  const dispatch = useDispatch();

  let serverUrl = "localhost:3000";
  let socket = io(serverUrl);

  const [isConnected, setIsConnected] = useState(socket.connected);
  const [benchmark, setBenchmark] = useState({});
  const [benchmark2, setBenchmark2] = useState({});

  React.useEffect(() => {
    dispatch(setConfig());
    socket.connect();
    const bencmarkListiner = (message) => {
      console.log("coming here benchmark");
      setBenchmark(message);
    };
    const bencmarkListiner2 = (message) => {
      console.log("coming here benchmark");
      setBenchmark2(message);
    };

    function onConnect() {
      console.log("connected");
      setIsConnected(true);
    }
    socket.on("connect", onConnect);
    socket.on("benchmark", bencmarkListiner);
    socket.on("benchmark2", bencmarkListiner2);

    return () => {
      socket.off("connect", onConnect);
      socket.off("benchmark", bencmarkListiner);
      socket.off("benchmark2", bencmarkListiner2);
    };
  }, []);

  const handleClick = (e) => {
    console.log("click");

    socket.timeout(2000).emit("benchmark", { file: "Beyoncé" }, () => {
      console.log("Emited");
    });
    socket.timeout(2000).emit("benchmark2", { file: "Beyoncé" }, () => {
      console.log("Emited");
    });
  };

  const config = useSelector((state) => state.config.config);
  if (config == null) {
    return <></>;
  }

  return (
    <>
      <div className="row" style={{ paddingTop: "1rem", paddingLeft: "1rem" }}>
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
          Start Comparision
        </button>
      </center>

      <div className="row">
        <div className="col-6">
          <center style={{ color: "white", paddingTop: "2rem" }}>
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

        <div className="col-6">
          <center style={{ color: "white", paddingTop: "2rem" }}>
            <h3>
              Percent Questions Correct: {benchmark2.percent_questions_correct}
            </h3>
            <h3>
              Number Questions Correct: {benchmark2.number_of_questions_correct}
            </h3>
            <h3>
              Number Questions Total: {benchmark2.number_of_questions_total}
            </h3>
            <h3>
              Average Time/Question: {benchmark2.average_time_per_question}
            </h3>
          </center>
          <div style={{ overflow: "scroll", height: "100vh", padding: "1rem" }}>
            {benchmark2.incorrect &&
              benchmark2.incorrect.map((data) => {
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
