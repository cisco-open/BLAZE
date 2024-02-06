import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import searchStyles from "./Search.module.css";

import { ModelSelect } from "../../components/modelSelect";
import { DatasetSelect } from "../../components/datasetSelect";
import { FunctionSelect } from "../../components/functionsSelect";

import { Sidebar } from "../../layouts/Sidebar";
import { Layout } from "../../layouts/Layout";

import { SearchCustom } from "./SearchCustom";
import { BenchmarkPage } from "./SearchBenchmark";
import { ComparisionPage } from "./SearchComparision";

export function SearchPage(props) {
  const config = useSelector((state) => state.config.config);
  const func = useSelector((state) => state.functions.AppFunction);
  console.log(config);
  console.log(func);
  if (config == null) {
    return <></>;
  }
  
  return (
    <>
      <Sidebar>
        <ModelSelect config={config} />
        <DatasetSelect config={config} />
        <hr />
        <FunctionSelect config={config} />
      </Sidebar>
      <div className={searchStyles.bdivider} />
      <Layout>
        {func==="custom" && <SearchCustom />}
        {func==="benchmark" && <BenchmarkPage />}
        {func==="comparing" && <ComparisionPage />}
      </Layout>
    </>
  );
}
