import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Records() {
    const navig = useNavigate();
  const [list, setList] = useState([]);
  const view = (date) => {
    navig(`/viewRecord/${date}`)
  }
  const getUserData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/getAllAttendance");
      const tableRows = [];
      for (let i = 0; i < response.data.Attendance.length; i++) {
        const check = response.data.Attendance[i].split("-");
        const check2 = check[1].split(".");
        console.log(check2);
        tableRows.push(
          <tr className="border-b border-gray-200">
            <td className="py-2">{i + 1}</td>
            <td className="py-2">{check2[0].replaceAll("_","-")}</td>
            <td className="py-2">
              <button
                className="bg-indigo-700 p-1 rounded-lg"
                onClick={() => {
                  view(check2[0]);
                }}
              >
                View
              </button>
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
        <h1 className="text-3xl font-bold mb-4 w-full ">Attendance List</h1>
        <table className="table-autojustify-center w-full sm:w-6/12">
          <thead>
            <tr>
              <th className="px-4 py-2">S.no</th>
              <th className="px-4 py-2">Date</th>
            </tr>
          </thead>
          <tbody>{list}</tbody>
        </table>
      </div>
    </div>
  );
}

export default Records;
