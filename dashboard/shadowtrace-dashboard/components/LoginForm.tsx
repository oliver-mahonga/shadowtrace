// components/LoginForm.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Login failed: Invalid credentials.');
      }

      const data = await response.json();
      
      // Store token (e.g., in localStorage or cookies for dashboard use)
      localStorage.setItem('access_token', data.access_token); 
      
      // Redirect to the secured dashboard
      router.push('/dashboard'); 

    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 animate-fadeIn transition-all duration-500">
      
      {/* Username Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">
          &gt; Username
        </label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md 
                     focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
          placeholder="user_identity_code..."
        />
      </div>

      {/* Password Field */}
      <div>
        <label className="block text-sm font-medium text-green-300 mb-1">
          &gt; Password
        </label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full px-4 py-2 border border-green-700 bg-gray-900/50 rounded-md 
                     focus:ring-2 focus:ring-green-500 focus:border-green-500 shadow-inner shadow-green-900/50"
          placeholder="secure_hash..."
        />
      </div>

      {/* Error Display */}
      {error && (
        <p className="text-red-500 text-sm bg-red-900/20 p-2 border border-red-700 rounded-md animate-pulse">
           ERROR: {error}
        </p>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={loading}
        className="w-full py-3 bg-green-700 text-gray-950 font-bold rounded-md hover:bg-green-600 transition-colors duration-300 
                   shadow-lg shadow-green-500/50 uppercase tracking-widest disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? 'AUTHENTICATING...' : 'EXECUTE LOGIN'}
      </button>
    </form>
  );
}