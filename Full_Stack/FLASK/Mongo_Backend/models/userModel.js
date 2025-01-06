const mongoose = require("mongoose");

const UserSchema = mongoose.Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    isAdmin: {
        type: Boolean,
        default:false
    },
},
    {
        timestamps: true,
    }
);

const userModel = mongoose.model("users", UserSchema);
module.exports = userModel; // Export as default
