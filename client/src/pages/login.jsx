import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const navig=useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {
    if (username === 'admin' && password === 'password') {
      window.localStorage.setItem("token",username);
      navig("/main-menu");
    } else {
      setError('Invalid username or password')
    }
  };
  useEffect(()=>{
    const token = window.localStorage.getItem('token');
    if(token)
      {
        navig("/main-menu")
      }
  })

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-300 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className='text-4xl text-indigo-700 select-none font-bold text-center'>
        FaceMark-ATTENDO
        </div>
        <div>
          <h2 className="mt-6 text-center text-4xl font-extrabold text-gray-900">Sign in to your account</h2>
        </div>
        {error && <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">{error}</div>}
        <div className="mt-8 space-y-6">
          <input
            type="text"
            className="border border-gray-300 p-3 w-full rounded-md"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            className="border border-gray-300 p-3 w-full rounded-md"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            onClick={handleLogin}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Sign in
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;