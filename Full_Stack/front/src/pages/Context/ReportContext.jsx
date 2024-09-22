// src/Context/ReportContext.jsx
import React, { createContext, useState } from 'react';

export const ReportContext = createContext();

export const ReportProvider = ({ children }) => {
  const [eval_res, setEvalRes] = useState([]);

  return (
    <ReportContext.Provider value={{ eval_res, setEvalRes }}>
      {children}
    </ReportContext.Provider>
  );
};
