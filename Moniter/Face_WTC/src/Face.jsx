import React, { useState, useEffect, useContext, useRef } from 'react'; 
import Peer from 'peerjs'; 
import io from 'socket.io-client';
import LoginContext from './LoginContext';
import styles from './Face.module.css'; // Import the module CSS

const FullscreenToggleComponent = ({ onFullscreenChange, setCheaterMode }) => {
  const [isFullscreen, setIsFullscreen] = useState(false);  
  const [switchCount, setSwitchCount] = useState(0);  
  
  useEffect(() => {
    if (onFullscreenChange) onFullscreenChange(isFullscreen);
  }, [isFullscreen, onFullscreenChange]);

  useEffect(() => {
    const handleFullscreenChange = () => {
      if (!document.fullscreenElement) {
        setSwitchCount(prevCount => {
          const newCount = prevCount + 1;
          if (newCount > 3) {
            setCheaterMode(true);
          }
          return newCount;
        });
      }
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setSwitchCount(prevCount => {
          const newCount = prevCount + 1;
          if (newCount > 3) {
            setCheaterMode(true);
          }
          return newCount;
        });
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  const enterFullscreen = async () => {
    try {
      await document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } catch (err) {
      console.log("Error attempting to enable fullscreen mode:", err);
    }
  };

  const exitFullscreen = async () => {
    try {
      await document.exitFullscreen();
      setIsFullscreen(false);
    } catch (err) {
      console.log("Error attempting to exit fullscreen mode:", err);
    }
  };

  const toggleFullscreen = () => {
    if (isFullscreen) {
      exitFullscreen();
    } else {
      enterFullscreen();
    }
  };

  return (
    <button className={styles.fullscreenButton} onClick={toggleFullscreen}>
      {isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'}
    </button>
  );
};

function Face() {
  const { LoggedAs } = useContext(LoginContext);
  const [peerId, setPeerId] = useState(null);
  const remoteVideoRef = useRef(null);
  const [remoteIdByValue, setRemoteIdByValue] = useState('');
  const [isRemoteVideo, setIsRemoteVideo] = useState(false);
  const peerRef = useRef(null);
  const [processedImage, setProcessedImage] = useState(null);
  const socket = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [cheaterMode, setCheaterMode] = useState(false);

  useEffect(() => {
    socket.current = io('http://localhost:5000', {
      transports: ['websocket'],
    });

    socket.current.on('processed_frame', (data) => {
      setProcessedImage(data.image);
    });

    return () => {
      socket.current.disconnect();
    };
  }, []);

  useEffect(() => {
    const peer = new Peer();
    peerRef.current = peer;

    peer.on('open', function (id) {
      setPeerId(id);
    });

    peer.on('call', function (call) {
      navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then((mediaStream) => {
          call.answer(mediaStream); 

          call.on('stream', function (remoteStream) {
            remoteVideoRef.current.srcObject = remoteStream; 
            setIsRemoteVideo(true); 
          });
        })
        .catch((err) => {
          console.error("Failed to get user media", err);
        });
    });
  }, []);

  const startVideo = async () => {
    captureFrame();
  };

  const captureFrame = () => {
    const video = remoteVideoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageBase64 = canvas.toDataURL('image/jpeg');

    socket.current.emit('frame', imageBase64);
    setTimeout(captureFrame, 100);
  };

  const callUser = (remotePeerId) => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then((mediaStream) => {
        const call = peerRef.current.call(remotePeerId, mediaStream); 

        call.on('stream', function (remoteStream) {
          remoteVideoRef.current.srcObject = remoteStream;
          setIsRemoteVideo(true); 
        });
      })
      .catch((err) => {
        console.error("Failed to get user media", err);
      });
  };

  if (cheaterMode) {
    return <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '48px', color: 'red' }}>You have failed to keep the FullScreen</div>;
  }

  return (
    <div className={styles.container}>
      <FullscreenToggleComponent
        onFullscreenChange={(isFullscreen) => {}}
        setCheaterMode={setCheaterMode}
      />
      <div className={styles.videoContainer}>
        <div className={styles.videoBlock}>
          <h1 className={styles.heading}>Name: {LoggedAs}</h1>
          <h1 className={styles.heading}>PeerId: {peerId}</h1>
          <input
            type="text"
            className={styles.inputField}
            value={remoteIdByValue}
            onChange={(e) => setRemoteIdByValue(e.target.value)}
          />
          <button className={styles.button} onClick={() => callUser(remoteIdByValue)}>Call</button>
        </div>

        <div className={styles.videoBlock}>
          <video
            ref={remoteVideoRef}
            autoPlay
            className={`${styles.video} ${isRemoteVideo ? styles.remoteVideoActive : ''}`}
          />
          <button className={styles.button} onClick={startVideo}>Click to Eye Detect</button>
          <canvas ref={canvasRef} className={styles.canvas}></canvas>

          {processedImage && <img className={styles.processedImage} src={processedImage} alt="Processed" />} 
        </div>
      </div>
    </div>
  );
}

export default Face;
