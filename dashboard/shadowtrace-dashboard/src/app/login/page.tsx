// app/login/page.tsx
'use client';

import { useState } from 'react';
import Header from '../../../components/Header';
import LoginForm from '../../../components/LoginForm';
import RegisterForm from '../../../components/RegisterForm';
// import Header from '../../components/Header';
// import LoginForm from '../../components/LoginForm';
// import RegisterForm from '../../components/RegisterForm';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen bg-gray-950 text-green-400 font-mono flex flex-col items-center justify-center p-4">
      
      {/* Header is included for navigation */}
      <Header /> 

      {/* Auth Container with animated borders and shadow */}
      <div 
        className="relative w-full max-w-md p-8 pt-12 mt-16 rounded-lg 
                   bg-gray-900/70 border border-green-700/50 shadow-2xl 
                   shadow-green-900/50 transition-all duration-500 hover:shadow-green-700/50"
      >
        
        <h1 className="text-3xl font-bold tracking-widest text-green-500 mb-6 text-center">
           ACCESS PROTOCOL
        </h1>

        {/* Tab Switcher: Dark, glowing buttons */}
        <div className="flex justify-center space-x-4 mb-8 border-b border-green-700/30 pb-2">
          <button
            onClick={() => setIsLogin(true)}
            className={`text-lg px-4 py-1 transition-all duration-300 ${
              isLogin 
                ? 'text-green-300 border-b-2 border-green-500 shadow-lg shadow-green-700/30'
                : 'text-gray-500 hover:text-green-500'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`text-lg px-4 py-1 transition-all duration-300 ${
              !isLogin 
                ? 'text-green-300 border-b-2 border-green-500 shadow-lg shadow-green-700/30'
                : 'text-gray-500 hover:text-green-500'
            }`}
          >
            Register
          </button>
        </div>

        {/* Conditional Form Rendering */}
        <div className="relative overflow-hidden min-h-[300px]">
            {isLogin ? 
                <LoginForm /> : 
                <RegisterForm onRegisterSuccess={() => setIsLogin(true)} />
            }
        </div>
        
      </div>
    </div>
  );
}