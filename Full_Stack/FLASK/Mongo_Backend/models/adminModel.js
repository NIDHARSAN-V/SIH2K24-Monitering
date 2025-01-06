const mongoose = require("mongoose");

const AdminSchema = mongoose.Schema({
    CandidateName: { type: String },
    CandidateEmail: { type: String },
    CandidateDomain: { type: String },
    Percentage: { type: String },
    CandidateSkills: [{ type: String }],
    resume: { data: Buffer, contentType: String },
},
);

const adminModel = mongoose.model("admin", AdminSchema);
module.exports = adminModel;
// const mongoose = require("mongoose");
// const UserDetailsSchema = new mongoose.Schema({
//     name: { type: String, required: true },
//     email: { type: String, required: true },
//     resumeFileId: { type: mongoose.Schema.Types.ObjectId, ref: 'Resume' },
// });
// const AdminSchema = mongoose.Schema({
//     name: {
//         type: String,
//         required: true,
//     },
//     email: {
//         type: String,
//         required: true,
//     },
//     password: {
//         type: String,
//         required: true,
//     },
//     UserDetails: {
//         type: [UserDetailsSchema], // This makes UserDetails an array of objects
//         required: true, // Ensure that at least one UserDetail is present
//     },
// },
//     {
//         timestamps: true,
//     }
// );

// const adminModel = mongoose.model("admin", AdminSchema);
// module.exports = adminModel; // Export as default
