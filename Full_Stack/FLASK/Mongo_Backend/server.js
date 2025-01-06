const express = require("express");
const app = express();
const cors = require("cors");
require("dotenv").config(); // Ensure this line is present
const dbConfig = require("./config/dbConfig"); // Assuming this file correctly sets up your MongoDB connection
app.use(express.json());

app.use(cors({
    origin: 'http://localhost:5173', // Replace with your frontend URL
    methods: ['POST', 'GET'],
}));

const userRoute = require("./routes/userRouter");
const adminRoute = require("./routes/adminRouter");
const path = require("path");

app.use("/api/user", userRoute);

app.use("/api/admin", adminRoute);

const port = process.env.PORT || 5500;

app.listen(port, () => console.log(`Node Express Server Started at ${port}!`));
