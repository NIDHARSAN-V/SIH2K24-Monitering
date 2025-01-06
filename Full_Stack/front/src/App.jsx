import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ResumeUpload from './pages/Resume_upload/ResumeUpload';
import QuestionsPage from './pages/QuestionsPage/QuestionsPage';
import { ResumeProvider } from './pages/Context/ResumeContext';
import Navbar from './pages/Navbar/Navbar';
import Report from './pages/Report/Report';
import { ReportProvider } from './pages/Context/ReportContext';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Admin from './pages/Admin/Admin';
function App() {
  return (
    <ResumeProvider>
      <ReportProvider>
        <Navbar />
        <Router>
          <Routes>
            <Route path="/" element={<ResumeUpload />} />
            <Route path='/login' element={<Login />} />
            <Route path='/admin' element={<Admin />} />
            <Route path='register' element={<Register />} />
            <Route path="/interview" element={<QuestionsPage />} />
            <Route path='/report' element={<Report />} />
          </Routes>
        </Router>
      </ReportProvider>
    </ResumeProvider>
  );
}

export default App;
