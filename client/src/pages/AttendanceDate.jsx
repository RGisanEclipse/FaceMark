import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

function AttendanceDate() {
    const params = useParams();
    const navig = useNavigate();
  const [list, setList] = useState([]);
  const view = (date) => {
    navig(`/viewRecord/${date}`)
  }
  const getUserData = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/custom_attendance",
        {
            custom_date:params.id
        }
      );
      console.log(response.data);
      const tableRows = [];
      for (let i = 0; i < response.data.l; i++) {
        tableRows.push(
          <tr className="border-b border-gray-200">
            <td className="py-2">{i + 1}</td>
            <td className="py-2">{response.data.names[i]}</td>
            <td className="py-2">{response.data.rolls[i]}</td>
            <td className="py-2">
              {response.data.times[i]}
            </td>
          </tr>
        );
      }
      setList(tableRows);
    } catch (error) {
      console.log(error);
    }
  };
  useEffect(() => {
    getUserData();
  }, []);
  return (
    <div className="bg-gray-300 h-screen w-full flex justify-center">
      <div className="flex flex-col items-center mx-auto px-4 w-full text-center">
        <h1 className="text-6xl font-bold text-indigo-600">FaceMark-Attendo</h1>
        <h1 className="text-3xl font-bold mb-4 w-full ">Attendance on {params.id.replaceAll("_","-")}</h1>
        <table className="table-autojustify-center w-full sm:w-6/12">
          <thead>
            <tr>
              <th className="px-4 py-2">S.no</th>
              <th className="px-4 py-2">Name</th>
              <th className="px-4 py-2">Roll no</th>
              <th className="px-4 py-2">Time</th>
            </tr>
          </thead>
          <tbody>{list}</tbody>
        </table>
      </div>
    </div>
  );
}

export default AttendanceDate;