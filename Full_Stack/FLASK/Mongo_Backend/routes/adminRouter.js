// routes/admin.js
const express = require('express');
const multer = require('multer');
const mongoose = require('mongoose');
const router = express.Router();
const AdminModel = require('../models/adminModel'); // Make sure to adjust the path
const SkillSchema = require("../models/skillSchema")
// Configure multer to use memory storage
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Route for saving resumes
router.post('/saveResume', upload.single('resume'), async (req, res) => {
    const { userDetail, resumeData } = req.body; // This will contain the JSON strings
    const parsedUserDetail = JSON.parse(userDetail);
    const parsedResumeData = JSON.parse(resumeData);

    if (!userDetail || !resumeData) {
        return res.status(400).json({ message: 'Missing userDetail or resumeData.' });
    }

    const { name, email } = parsedUserDetail;
    const { mapped_domain, match_percentage, matched_skills } = parsedResumeData;

    const adminEntry = new AdminModel({
        resume: {
            data: req.file.buffer,
            contentType: req.file.mimetype,
        },
        CandidateName: name,
        CandidateEmail: email,
        CandidateDomain: mapped_domain,
        Percentage: match_percentage,
        CandidateSkills: matched_skills
    });

    try {
        const result = await adminEntry.save();
        res.status(200).json({
            message: 'Resume uploaded successfully!',
            id: result._id,
        });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Error saving resume to database.' });
    }
});


// Assuming AdminModel contains the user's email and resume data
router.get('/getResume/:email', async (req, res) => {
    try {
        // Find the resume based on the email field
        const resume = await AdminModel.findOne({ CandidateEmail: req.params.email });

        if (!resume) {
            return res.status(404).json({ message: 'Resume not found for this email.' });
        }

        // Set the response headers for PDF download
        res.set({
            'Content-Type': resume.resume.contentType,  // Assuming resume has contentType like 'application/pdf'
            'Content-Disposition': `attachment; filename="resume.pdf"`,  // Adjust filename as needed
        });

        // Send the resume PDF data and the resume ID
        res.status(200).json({
            resumeId: resume._id,
            resumeData: resume.resume.data // Assuming resume stores the PDF data here
        });

    } catch (err) {
        console.error(err);
        res.status(500).json({ error: 'Error retrieving resume from database.' });
    }
});
router.get('/getAllCandidates', async (req, res) => {

    const CandidateDetails = await AdminModel.find({});

    return res.send(CandidateDetails);
});
router.post('/getParagraph', async (req, res) => {
    const skill = req.body.skill.trim();
    console.log("Received skill:", skill);

    // Look for the skill in the database
    const skillDoc = await SkillSchema.findOne({ skill: skill });

    if (!skillDoc) {
        // If skill is not found, return a "not found" string instead of a 404 error
        return res.send('not found');
    }

    console.log("Found paragraph for skill:", skillDoc);
    return res.send(skillDoc.paragraph);
});


module.exports = router;

// routes/admin.js

