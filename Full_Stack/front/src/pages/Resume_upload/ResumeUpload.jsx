import React, { useState, useContext, useEffect } from 'react';
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
  const [uploadedResumeId, setUploadedResumeId] = useState('');
  const [userDetail, setUserDetail] = useState('');
  useEffect(() => {
    const getUser = async () => {
      const token = localStorage.getItem('token');
      const response = await axios.post("http://localhost:5500/api/user/getUser",
        {},
        {
          headers: {
            Authorization: token,
          },
        }
      );
      console.log(response.data);
      setUserDetail(response.data[0]);
    }
    getUser();
  }, []
  );

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
      console.log(response.data)


      if (response.status === 200) {
        setResumeData(response.data);
        setIsFileUploaded(true);
        formData.append('userDetail', JSON.stringify(userDetail));
        formData.append('resumeData', JSON.stringify(response.data));
        try {
          const response2 = await axios.post('http://localhost:5500/api/admin/saveResume',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            });
          setUploadedResumeId(response2.data.id); // Store the ID of the uploaded resume
        }
        catch (error) {
          console.log(error);
        }


      } else {
        alert("Failed to upload the resume.");
      }
    } catch (error) {
      alert("Error uploading the resume: " + error.response?.data?.error || error.message);
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

  const viewResume = async () => {
    if (!userDetail.email) {
      alert("User email not found.");
      return;
    }

    try {
      // Fetch resume by email
      const response = await axios.get(`http://localhost:5500/api/admin/getResume/${userDetail.email}`, {
        responseType: 'blob', // Expecting a binary response (PDF data as blob)
      });

      // Extract resume data from response
      const blob = new Blob([response.data.resumeData], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);

      // Open the PDF in a new tab
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'resume.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();

      // Optionally, you can save the resumeId if needed for further operations
      setUploadedResumeId(response.data.resumeId);

    } catch (error) {
      console.error("Error retrieving the resume:", error);
      alert("Error retrieving the resume.");
    }
  };


  return (
    <div className={styles.uploadPage}>
      <h1 className={styles.heading}>Resume Details</h1>
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
          <div>
            <button
              onClick={viewResume}
              className={styles.uploadButton}
            >
              View Resume
            </button>
            <button onClick={handleRemoveFile} className={styles.uploadButton}>
              Remove File
            </button>

          </div>
        )}
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
    </div>
  );
}

export default ResumeUpload;
