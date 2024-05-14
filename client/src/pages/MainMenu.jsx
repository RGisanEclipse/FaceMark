import { UserPlus, PencilLine, UsersFour, AddressBook } from "phosphor-react";
import React from "react";
import { useNavigate } from "react-router-dom";

const MainMenu = () => {
  const navig = useNavigate();
  const logout = () => {
    window.localStorage.removeItem("token");
    navig("/");
  };
  return (
    <div className="relative w-full bg-slate-300 min-h-screen h-full">
      <div className="flex justify-center items-center h-screen w-full cursor-pointer bg-slate-300 flex-col">
        <div className="text-6xl text-indigo-700 font-bold select-none truncate mb-8">
          FaceMark-Attendo
        </div>
        <div className="grid grid-cols-2 gap-6 lg:grid-cols-4">
          <div className="bg-white rounded-lg shadow-md p-6 hover:bg-indigo-700 hover:text-white cursor-pointer" onClick={()=>{navig("/add-student")}}>
            <UserPlus size={32} />
            <h2 className="text-xl font-semibold mb-4">Add</h2>
            <p className=" hover:text-white">Add Student</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 hover:bg-indigo-700 hover:text-white cursor-pointer" onClick={()=>{navig("/mark")}}>
            <PencilLine size={32} />
            <h2 className="text-xl font-semibold mb-4">Mark</h2>
            <p className=" hover:text-white">Mark Attendance</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 hover:bg-indigo-700 hover:text-white cursor-pointer" onClick={()=>{navig("/studentsList")}}>
            <UsersFour size={32} />
            <h2 className="text-xl font-semibold mb-4">UserList</h2>
            <p className=" hover:text-white">Show user list</p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6 hover:bg-indigo-700 hover:text-white cursor-pointer" onClick={()=>{navig("/attendance")}}>
          <AddressBook size={32} />
            <h2 className="text-xl font-semibold mb-4">Records</h2>
            <p className=" hover:text-white">Show Attendance</p>
          </div>
          <button
            className="absolute top-2 right-2 bg-indigo-700 p-2 rounded-lg text-white hover:bg-indigo-800 "
            onClick={logout}
          >
            logout
          </button>
        </div>
      </div>
    </div>
  );
};

export { MainMenu };
