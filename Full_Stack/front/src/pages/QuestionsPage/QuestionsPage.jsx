import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import styles from './QuestionsPage.module.css';
import { ResumeContext } from '../Context/ResumeContext';
import { ReportContext } from '../Context/ReportContext';
import PulseLoader from 'react-spinners/PulseLoader';
import { useNavigate } from 'react-router-dom';
import { FaMicrophone, FaMicrophoneSlash } from 'react-icons/fa';
import socket from '../../socket';
function QuestionsPage() {
  const { resumeData } = useContext(ResumeContext);
  const { eval_res, setEvalRes } = useContext(ReportContext);
  const [answer, setAnswer] = useState('');
  const [mapDomain, setMapDomain] = useState([]);
  const [mapSkills, setMapSkills] = useState([]);
  const [setOfQuestions, setSetOfQuestions] = useState([]);
  const [askq, setAskq] = useState(false);
  const [qindex, setQindex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(90);
  const [dom_count, setdom_count] = useState(0);
  const [loading, setLoading] = useState(false);
  const [final_dom, setfinal_dom] = useState('');
  const [micOn, setMicOn] = useState(false);
  const [showTranscript, setShowTranscript] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [qnaArray, setQnaArray] = useState([]); // Store all QNA for each skill (indexed by dom_count)

  const navigate = useNavigate();

  useEffect(() => {
    setMapDomain(resumeData.mapped_domain);
    setMapSkills(resumeData.matched_skills);
  }, [resumeData]);

  useEffect(() => {
    socket.on('qnaGenerated', ({ skill, qna }) => {
      console.log('QNA Generated for skill:', skill, qna);

      const qaString = qna[0]; // Extract the qna string
      const questionsAndAnswers = processQuestionsAndAnswers(qaString);
      console.log("QBA", questionsAndAnswers)
      if (dom_count === 0) {
        // Directly display questions for the first skill
        if (!askq) {
          setSetOfQuestions(questionsAndAnswers);
          setAskq(true);
          setLoading(false);
        }

        else {
          const updatedQnaArray = [...qnaArray];
          updatedQnaArray[dom_count] = questionsAndAnswers;
          console.log(updatedQnaArray[dom_count]);
          setQnaArray(updatedQnaArray);
          setLoading(false);
        }
      }
    });

    socket.on('qnaStatus', ({ skill, message }) => {
      console.warn(`Status for ${skill}:`, message);
      if (message.includes('not found')) {
        handlenextDomain(); // Call your function to proceed to the next domain
      }
    });

    socket.on('generationComplete', () => {
      console.log('All skills processed.');
    });

    socket.on('error', (error) => {
      console.error('Socket Error:', error);
    });

    return () => {
      socket.off('qnaGenerated');
      socket.off('qnaStatus');
      socket.off('generationComplete');
      socket.off('error');
    };
  }, [askq, dom_count]);

  useEffect(() => {
    if (askq && setOfQuestions.length > 0) {
      setAnswer('');
      setTranscript('');
      setMicOn(false)
      setTimeLeft(20);
      const timer = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);

      const timeout = setTimeout(() => {
        submitAnswer();
      }, 20000); // Change timeout to 20,000 milliseconds

      return () => {
        setMicOn(false);
        clearInterval(timer);
        clearTimeout(timeout);
      };
    }
  }, [qindex, askq, setOfQuestions.length]);


  const submitAnswer = () => {
    const updatedQuestions = [...setOfQuestions];
    updatedQuestions[qindex].candidate_answer = answer || 'NULL';
    setSetOfQuestions(updatedQuestions);

    setAnswer('');
    setTranscript('');
    setShowTranscript(false);
    console.log("QINDEX", qindex);
    if (qindex < setOfQuestions.length - 1) {
      setQindex(qindex + 1);

      setAnswer('');
      setTranscript('');
    } else {
      setAskq(false);
      setQindex(0);

      console.log('All questions answered:', updatedQuestions);
    }
  };


  const handleTranscriptReady = (transcriptText) => {
    setAnswer(transcriptText);
    setTranscript(transcriptText);
    setShowTranscript(true);
  };

  const handleConfirmTranscript = () => {
    submitAnswer();
  };

  const handleEditTranscript = () => {
    setShowTranscript(false);
  };

  const toggleMic = (status) => {
    setMicOn(status);
    if (status) {
      startListening();
    } else {
      stopListening();
    }
  };

  // Web Speech API Functions
  const startListening = () => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new window.webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = false;
      recognition.lang = 'en-IN';

      recognition.onstart = () => {
        setMicOn(true);
      };

      recognition.onend = () => {
        setMicOn(false);
      };

      recognition.onresult = (event) => {
        const transcriptResult = Array.from(event.results)
          .map((result) => result[0])
          .map((result) => result.transcript)
          .join('');
        handleTranscriptReady(transcriptResult);
      };

      recognition.onerror = (event) => {
        console.error('Speech Recognition Error:', event.error);
      };

      recognition.start();
      window.recognitionInstance = recognition;
    } else {
      console.error('Web Speech API is not supported in this browser.');
    }
  };

  const stopListening = () => {
    if (window.recognitionInstance) {
      window.recognitionInstance.stop();
    }
  };

  const handleEvaluate = async () => {
    try {
      setLoading(true);
      console.log('In Evaluate');
      console.log(setOfQuestions);
      const res = await axios.post('http://localhost:5001/api/evaluate', { QandA: setOfQuestions });
      console.log('Evaluation Result:', res.data);
      const percentage1 = res.data.QandA_Eval.All_Average;
      const percentageGem = res.data.QandA_Eval.Percentage_Gem;
      const percentageSBert = res.data.QandA_Eval.Percentage_SBert;

      setEvalRes((prevEvalRes) => [
        ...prevEvalRes,
        {
          domain: final_dom,
          percentage_avg: percentage1,
          percentage_gem: percentageGem,
          percentage_sbert: percentageSBert,
        },
      ]);
      setdom_count(dom_count + 1);
      setLoading(false);
    } catch (error) {
      console.error('Error evaluating answers:', error);
      alert('Error evaluating answers. Check console for details.');
    }
  };
  // When receiving data from Flask, process the Q&A

  const processQuestionsAndAnswers = (qaString) => {
    const qaArray = qaString.split('\n\n').map((item) => {
      const questionAnswer = item.split('\n');
      return {
        question: questionAnswer[0]?.replace(/^\d+\.\s*Question:\s*/, '').trim(), // Remove "1. Question:" from the question
        reference_answer: questionAnswer[1]?.replace('Answer:', '').trim(), // Remove "Answer:" from the answer
      };
    });
    return qaArray;
  };


  const handlePushToNode = () => {
    const skillsToProcess = resumeData.matched_skills;
    const domain = resumeData.mapped_domain[dom_count];
    setLoading(true);
    socket.emit('generateQuestions', { inp: domain, Domain: resumeData.mapped_domain, Skills: skillsToProcess });
  };

  const handlenextDomain = () => {
    setLoading(true);
    const nextQNA = qnaArray[dom_count];

    setSetOfQuestions(nextQNA);
    setAskq(true);
    setLoading(false);
    setdom_count(dom_count + 1);

  };
  return (
    <div className={styles.uploadPage}>
      <h1 className={styles.heading}>Interview Question</h1>

      {loading ? (
        <PulseLoader color="#ac04ff" />
      ) : (
        <>
          {askq && setOfQuestions.length > 0 && qindex < setOfQuestions.length ? (
            <div className={styles.answerContainer}>
              <div className={styles.questionContainer}>
                <p id="questionText" className={styles.questionText}>
                  {qindex}.) {setOfQuestions[qindex].question}
                </p>
                <p className={styles.timer}>Time left: {timeLeft} seconds</p>
              </div>
              <div className={styles.micControls}>
                <p>Microphone: {micOn ? 'On' : 'Off'}</p>
                <button onClick={() => toggleMic(!micOn)} className={styles.micButton}>
                  {micOn ? <FaMicrophoneSlash size={24} /> : <FaMicrophone size={24} />}
                </button>
              </div>

              <div className={styles.textInputContainer}>
                <input
                  type="text"
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  placeholder="Type your answer here"
                  className={styles.textInput}
                />
                <button onClick={submitAnswer} className={styles.uploadButton}>
                  Submit
                </button>
              </div>

              {showTranscript && micOn && (
                <div className={styles.transcriptContainer}>
                  <p>Transcript: {transcript}</p>
                  <button onClick={handleConfirmTranscript} className={styles.uploadButton}>
                    Confirm Transcript
                  </button>
                  <button onClick={handleEditTranscript} className={styles.uploadButton}>
                    Edit Transcript
                  </button>
                </div>
              )}
            </div>
          ) : (
            <p>{askq ? 'No more questions available.' : 'Click the button to start.'}</p>
          )}

          {resumeData && (
            <div className={styles.resultsContainer}>
              <h1>Question in Domain: {dom_count}</h1>
              <button onClick={handlePushToNode} className={styles.Startbutton}>
                Click To Start
              </button>
              <button onClick={handlenextDomain} className={styles.Startbutton}>
                Go to Next Domain
              </button>
              <br />
              <br />
              <br />
              <button onClick={handleEvaluate} className={styles.Evalbutton}>
                Evaluate
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default QuestionsPage;