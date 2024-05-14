import axios from "axios";
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Mark() {
    const navig = useNavigate();
    const [load,setLoad] = useState(false);
    const markAttendance = async() => {
        try {
            setLoad(true);
            const response = await axios('http://127.0.0.1:5000/start');
            console.log(response.data);
            setLoad(false);
            navig('/main-menu');
        } catch (error) {
            setLoad(false);
            console.log(error.message);
        }
    }
  return <div className="flex items-center justify-center w-full h-screen">
    {!load && <button className="text-6xl bg-indigo-700 text-white p-2 rounded-lg" onClick={markAttendance}>
        Mark Attendance
    </button>}
    {load && <button className="text-6xl bg-indigo-800 text-white p-2 rounded-lg" disabled>
        Camera Open...
    </button>}
  </div>;
}

export { Mark };
