import React from 'react';
import './Navbar.css'; // Import the CSS file

const Navbar = () => {
    return (
        <div className="navbar">
            <div className="left">
                <a href="#" className="legacy">Legacy</a>
            </div>
            <div className="center">
                <span className="interv">IntervAI</span>
            </div>
            <div className="right">
                <a href="#" className="hover-effect">ResumeUp</a>
                
                <a href="#" className="hover-effect">Report</a>
            </div>
        </div>
    );
};

export default Navbar;
