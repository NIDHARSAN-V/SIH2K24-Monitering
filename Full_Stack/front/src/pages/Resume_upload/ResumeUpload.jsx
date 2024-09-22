import React, { useState, useContext } from 'react';
import axios from 'axios';
import styles from './ResumeUpload.module.css';
import { useNavigate } from 'react-router-dom';
import { ResumeContext } from '../Context/ResumeContext';

function ResumeUpload() {
  const navigate = useNavigate();
  const { resumeData, setResumeData } = useContext(ResumeContext);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isFileUploaded, setIsFileUploaded] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Please select a resume file first.");
      return;
    }

    const formData = new FormData();
    formData.append('resume', selectedFile);

    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/uploadResume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        setResumeData(response.data);
        setIsFileUploaded(true);
      } else {
        alert("Failed to upload the resume.");
      }
    } catch (error) {
      alert("Error uploading the resume.");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setResumeData(null);
    setIsFileUploaded(false);
  };

  const startInterview = () => {
    navigate('/interview');
  };

  return (
    <div className={styles.uploadPage}>
      <h1 className={styles.heading}>Upload Your Resume</h1>
      <div className={styles.uploadContainer}>
        {!isFileUploaded && (
          <>
            <input
              type="file"
              onChange={handleFileChange}
              className={styles.inputFile}
              accept=".pdf"
            />
            <button
              onClick={handleUpload}
              className={styles.uploadButton}
              disabled={isLoading}
            >
              {isLoading ? 'Uploading...' : 'Upload Resume'}
            </button>
          </>
        )}
        {isFileUploaded && (
          <button onClick={handleRemoveFile} className={styles.uploadButton}>
            Remove File
          </button>
        )}
      </div>

      {resumeData && (
        <div className={styles.resultsContainer}>
          <h2 className={styles.resultsHeading}>Resume Analysis Results:</h2>
          <p><strong>Extracted Domain:</strong> {resumeData.domain}</p>
          <p><strong>Mapped Domain:</strong> {resumeData.mapped_domain}</p>
          <p><strong>Match Percentage:</strong> {resumeData.match_percentage}%</p>
        
          <div className={styles.skillsWrapper}>
            <div className={styles.skillsContainer}>
              <h3 className={styles.skillsHeading}>Extracted Skills:</h3>
              <div className={styles.skillsList}>
                {resumeData.skills.map((skill, index) => (
                  <div key={index} className={styles.skillItem}>{skill}</div>
                ))}
              </div>
            </div>

            <div className={styles.skillsContainer}>
              <h3 className={styles.skillsHeading}>Matched Skills:</h3>
              <div className={styles.skillsList}>
                {resumeData.matched_skills.map((skill, index) => (
                  <div key={index} className={styles.skillItem}>{skill}</div>
                ))}
              </div>
            </div>
          </div>

          <button 
            onClick={startInterview} 
            className={`${styles.uploadButton} ${styles.start__interview}`}
          >
            Start Interview
          </button>
        </div>
      )}
    </div>
  );
}

export default ResumeUpload;
