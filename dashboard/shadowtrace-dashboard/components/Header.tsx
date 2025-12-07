// components/Header.tsx
'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 p-4 border-b border-green-700/50 backdrop-blur-sm shadow-lg shadow-green-900/10">
      <div className="container mx-auto flex justify-between items-center">
        
       
        <Link href="/" className="text-2xl font-bold tracking-widest text-green-500 hover:text-green-300 transition-colors">
          SHADOWTRACE
        </Link>
        
        {/* Navigation/Auth Buttons */}
        <nav className="space-x-4">
          <Link 
            href="/dashboard" 
            className="text-sm px-3 py-1 border border-green-700 rounded-md hover:bg-green-900/30 transition-all"
          >
            Dashboard
          </Link>
          <Link 
            href="/login" 
            className="text-sm px-4 py-1.5 bg-green-700 text-gray-950 font-bold rounded-md hover:bg-green-600 transition-colors shadow-green-500/50 shadow-md"
          >
            Login / Access
          </Link>
        </nav>
      </div>
    </header>
  );
}