const mongoose = require("mongoose");

const SkillSchema = new mongoose.Schema({
    skill: { type: String, required: true, unique: true },
    paragraph: { type: String, required: true }
});

const skillModule = mongoose.model('Materials', SkillSchema,'Materials');
module.exports = skillModule;
