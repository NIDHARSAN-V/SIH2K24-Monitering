const express = require('express');
const axios = require('axios');
const cors = require('cors');
const fs = require("fs");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.use(cors({
    origin: `http://localhost:5173`,  
    methods: ['POST', 'GET'], 
    credentials: true        
}));

app.post('/api/generate', async (req, res) => {
    console.log(req.body);
    var domain = req.body.inp;
    // domain = "react"
    console.log("================================" , domain);
    
    const data = fs.readFileSync('contexts.json');
    const Contexts = JSON.parse(data);
    
    const contextEntries = Object.entries(Contexts[domain] || {});
    let allQuesAns = [];

    for (const [key, context] of contextEntries) {
        console.log(context);
        
        try {
            const response = await axios.post('http://localhost:5004/api/generate', {
                inp: context
            });

            // Extract the questions and answers array from the response
            const questionsAndAnswers = response.data.questions_and_answers;

            // Merge it into the allQuesAns array
            allQuesAns = allQuesAns.concat(questionsAndAnswers);

        } catch (error) {
            console.error('Error fetching data from Flask API:', error);
            res.status(500).json({ error: 'Error fetching data from Flask API' });
            return;
        }
    }
    
    // Return the merged array
    res.json(allQuesAns);
});


app.use("/api/evaluate" , async function(req,res)
{
    try{
           console.log(req.body)

           const QandA = req.body.QandA
        //    console.log(QandA)
           const response_eval = await axios.post("http://localhost:5003/evaluate" , {"QandA":QandA})
        //    console.log(response_eval.data)
           res.json({"QandA_Eval":response_eval.data})
    }
    catch(error)
    {
        console.log(error)
    }
})

app.listen(5001, () => {
    console.log(`Server is running on 5001`);
});
