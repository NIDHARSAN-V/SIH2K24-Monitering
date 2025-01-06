const express = require('express');
const axios = require('axios');
const cors = require('cors');
const { Server } = require('socket.io');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 3000;

const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: 'http://localhost:5173',
        methods: ['GET', 'POST']
    }
});

app.use(express.json());
app.use(cors({
    origin: 'http://localhost:5173',
    methods: ['POST', 'GET'],
    credentials: true
}));

io.on('connection', (socket) => {
    console.log('Client connected:', socket.id);

    socket.on('generateQuestions', async ({ inp, Domain, Skills }) => {
        if (!Array.isArray(Skills) || Skills.length === 0) {
            socket.emit('error', { error: "Skills must be a non-empty array" });
            return;
        }

        for (const skill of Skills) {
            try {
                const paraResponse = await axios.post('http://localhost:5500/api/admin/getParagraph', { skill });

                if (paraResponse.data === 'not found') {
                    socket.emit('qnaStatus', { skill, status: 'not found', message: `No paragraph found for ${skill}` });
                    continue;
                }

                const flaskData = { data: paraResponse.data };
                const response = await axios.post('http://localhost:5004/api/generate', flaskData, {
                    headers: { 'Content-Type': 'application/json' }
                });

                const qna = response.data.questions_and_answers;
                socket.emit('qnaGenerated', { skill, qna });

            } catch (error) {
                console.error(`Error processing skill "${skill}":`, error.message);
                socket.emit('error', { error: `Error generating questions for skill: ${skill}` });
            }
        }

        socket.emit('generationComplete');
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected:', socket.id);
    });
});




app.use("/api/evaluate", async function (req, res) {
    try {
        console.log(req.body)

        const QandA = req.body.QandA
        //    console.log(QandA)
        const response_eval = await axios.post("http://localhost:5003/evaluate", { "QandA": QandA })
        //    console.log(response_eval.data)
        res.json({ "QandA_Eval": response_eval.data })
    }
    catch (error) {
        console.log(error)
    }
})
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
