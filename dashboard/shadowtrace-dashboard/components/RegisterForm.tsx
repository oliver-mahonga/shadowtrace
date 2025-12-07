// components/RegisterForm.tsx
'use client';

import { useState } from 'react';

interface RegisterFormProps {
    onRegisterSuccess: () => void;
}

export default function RegisterForm({ onRegisterSuccess }: RegisterFormProps) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, confirm_password: confirmPassword }),
      });

      const data = await response.json();

      if (!response.ok) {
        // Handle validation errors from FastAPI/Pydantic
        const errorDetail = data.detail 
            ? (Array.isArray(data.detail) ? data.detail[0].msg : data.detail) 
            : 'Registration failed.';
        throw new Error(errorDetail);
      }
      
      setSuccess('User profile created. Redirecting to login...');
      setTimeout(onRegisterSuccess, 2000); // Redirect to login after 2 seconds

    } catch (err: any) {
      setError(err.message || 'An unknown error occurred during registration.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 animate-fadeIn transition-all duration-500">
      
      {/* Username Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">&gt; Username</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required placeholder="alias_name"
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
        />
      </div>

      {/* Email Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">&gt; Email Address</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="user@domain.net"
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
        />
      </div>

      {/* Password Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">&gt; Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="generate_strong_password"
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
        />
      </div>

      {/* Confirm Password Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">&gt; Confirm Password</label>
        <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required placeholder="re_enter_hash"
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
        />
      </div>

      {/* Status Display */}
      {error && (
        <p className="text-red-500 text-sm bg-red-900/20 p-2 border border-red-700 rounded-md animate-pulse">
           ERROR: {error}
        </p>
      )}
      {success && (
        <p className="text-green-500 text-sm bg-green-900/20 p-2 border border-green-700 rounded-md">
           SUCCESS: {success}
        </p>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading || !!success}
        className="w-full py-3 bg-green-700 text-gray-950 font-bold rounded-md hover:bg-green-600 transition-colors duration-300 
                   shadow-lg shadow-green-500/50 uppercase tracking-widest disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'REGISTERING USER...' : 'INITIATE REGISTRATION'}
      </button>
    </form>
  );
}