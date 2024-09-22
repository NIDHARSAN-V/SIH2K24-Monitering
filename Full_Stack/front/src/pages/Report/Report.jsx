// src/components/Report.jsx
import React, { useContext } from 'react';
import { ReportContext } from '../Context/ReportContext';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import styles from './Report.module.css';

function Report() {
  const { eval_res } = useContext(ReportContext);

  const downloadPDF = () => {
    const doc = new jsPDF();

    doc.text('Evaluation Report', 20, 10);
    
    const tableColumn = ["Domain", "Percentage_Average","Percentage_Gem","Percentage_SBert"];
    const tableRows = [];

    eval_res.forEach(result => {
      const resultData = [
        result.domain,
        `${result.percentage_avg}%`,
        `${result.percentage_gem}%`,
        `${result.percentage_sbert}%`

      ];
      tableRows.push(resultData);
    });

    doc.autoTable({
      head: [tableColumn],
      body: tableRows,
      startY: 20,
      theme: 'grid',
    });

    doc.save("evaluation_report.pdf");
  };

  return (
    <div className={styles.outer}>
      <div className={styles.reportContainer}>
        <h1 className={styles.heading}>Evaluation Report</h1>
        
          <>
            <table className={styles.reportTable}>
              <thead>
                <tr>
                  <th>Domain</th>
                  <th>Percentage_Average</th>
                  <th>Percentage_Gem</th>
                  <th>Percentage_Sbert</th>
                </tr>
              </thead>
              <tbody>
                {eval_res.map((result, index) => (
                  <tr key={index}>
                    <td>{result.domain}</td>
                    <td>{result.percentage_avg}</td>
                    <td>{result.percentage_gem}</td>
                    <td>{result.percentage_sbert}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <button onClick={downloadPDF} className={styles.downloadButton}>Download as PDF</button>
          </>
    
          
    
      </div>
    </div>
  );
}

export default Report;
