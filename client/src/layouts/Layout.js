import React, { useState, useEffect } from "react";
import styles from "./Layout.module.css";
export function Layout({ children }) {
  return (
    <>
      <div className={styles.bdivider} />
      <div className="bg-dark" style={{ width: "100%" }}>
        {children}
      </div>
    </>
  );
}
