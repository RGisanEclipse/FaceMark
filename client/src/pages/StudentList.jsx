import React, { useState, useEffect } from "react";
import axios from "axios";

function StudentList() {
  const [list, setList] = useState([]);
  const [load, setLoad] = useState(false);
  const deleteUser = async (userId) => {
    console.log(userId);
    try {
      setLoad(true);
      const response = await axios.post("http://127.0.0.1:5000/deleteuser", {
        user: userId,
      });
      const tableRows = [];
      for (let i = 0; i < response.data.l; i++) {
        tableRows.push(
          <tr className="border-b border-gray-200">
            <td className="py-2">{i + 1}</td>
            <td className="py-2">{response.data.names[i]}</td>
            <td className="py-2">{response.data.rolls[i]}</td>
            <td className="py-2">
              <button
                className="bg-indigo-700 p-1 rounded-lg"
                disabled={load}
                onClick={() => {
                  deleteUser(response.data.userlist[i]);
                }}
              >
                delete
              </button>
            </td>
          </tr>
        );
      }
      setList(tableRows);
      setLoad(true);
    } catch (error) {
      setLoad(false);
    }
  };
  const getUserData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/listusers");
      const tableRows = [];
      for (let i = 0; i < response.data.l; i++) {
        tableRows.push(
          <tr className="border-b border-gray-200">
            <td className="py-2">{i + 1}</td>
            <td className="py-2">{response.data.names[i]}</td>
            <td className="py-2">{response.data.rolls[i]}</td>
            <td className="py-2">
              <button
                className="bg-indigo-700 p-1 rounded-lg"
                disabled={load}
                onClick={() => {
                  deleteUser(response.data.userlist[i]);
                }}
              >
                delete
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
        <h1 className="text-3xl font-bold mb-4 w-full ">Students List</h1>
        <table className="table-autojustify-center w-full sm:w-6/12">
          <thead>
            <tr>
              <th className="px-4 py-2">S.no</th>
              <th className="px-4 py-2">Name</th>
              <th className="px-4 py-2">Roll no</th>
              <th className="px-4 py-2">Options</th>
            </tr>
          </thead>
          <tbody>{list}</tbody>
        </table>
      </div>
    </div>
  );
}

export default StudentList;
