import Peer from 'peerjs';
import React, { useContext, useEffect, useRef, useState } from 'react';
import "./App.css";
import LoginContext from './LoginContext';

function Face() {
  const { LoggedAs } = useContext(LoginContext);
  const [peerId, SetPeerId] = useState(null);
  const remoteVideoRef = useRef(null);
  const [remoteIdByValue, setRemoteIdByValue] = useState('');
  const peerRef = useRef(null);

  useEffect(() => {
    const peer = new Peer();
    peerRef.current = peer;

    peer.on('open', function (id) {
      SetPeerId(id);
    });

    peer.on('call', function (call) {
      // Just accept the call but don't respond with screen sharing
      call.answer(); 

      call.on('stream', function (remoteStream) {
        remoteVideoRef.current.srcObject = remoteStream; // Show remote screen
      });
    });
  }, []);

  const callUser = function (remotePeerId) {
    navigator.mediaDevices.getDisplayMedia({ video: true, audio: false })
      .then((mediaStream) => {
        const call = peerRef.current.call(remotePeerId, mediaStream); // Initiate the call with screen sharing

        call.on('stream', function (remoteStream) {
          remoteVideoRef.current.srcObject = remoteStream; // Show remote screen
        });
      })
      .catch((err) => {
        console.error("Failed to get display media", err);
      });
  };

  return (
    <div>
      <div>
        <h1>Name: {LoggedAs}</h1>
        <h1>PeerId: {peerId}</h1>
        <input
          type="text"
          value={remoteIdByValue}
          onChange={(e) => setRemoteIdByValue(e.target.value)}
        />
        <button onClick={() => callUser(remoteIdByValue)}>Call</button>
        <br />
      </div>
      <div>
        <video ref={remoteVideoRef} autoPlay />
      </div>
    </div>
  );
}

export default Face;