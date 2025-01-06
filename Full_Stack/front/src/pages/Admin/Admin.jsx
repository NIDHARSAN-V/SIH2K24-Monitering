import React, { useEffect, useState } from 'react'
import axios from 'axios';
function Admin() {
    const [candidateDetail, setCandidateDetail] = useState([]);
    useEffect(() => {
        const getCandidate = async () => {
            const token = localStorage.getItem('token');
            const response = await axios.get("http://localhost:5500/api/admin/getAllCandidates")
            console.log(response.data);
            setCandidateDetail(response.data[0]);
        }
        getCandidate();
    }, []
    );
    return (
        <div>Admin</div>
    )
}

export default Admin