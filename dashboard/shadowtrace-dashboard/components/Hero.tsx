// components/Hero.tsx
import { Link } from 'lucide-react';
import React from 'react';

// A simple utility for a "glitch" line effect
const GlitchLine = () => (
    <div className="h-0.5 w-full bg-green-700/50 my-8 shadow-green-500/20 shadow-xl animate-pulse"></div>
);

export default function Hero() {
  return (
    <section className="relative flex flex-col items-center justify-center pt-40 pb-20 text-center">
      
      {/* Subtle Background Grid/Lines */}
      <div className="absolute inset-0 opacity-10">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="smallGrid" width="8" height="8" patternUnits="userSpaceOnUse">
              <path d="M 8 0 L 0 0 0 8" fill="none" stroke="currentColor" strokeWidth="0.5"/>
            </pattern>
            <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse">
              <rect width="80" height="80" fill="url(#smallGrid)"/>
              <path d="M 80 0 L 0 0 0 80" fill="none" stroke="currentColor" strokeWidth="1"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>

      <div className="relative z-10 max-w-4xl px-4">
        <h1 className="text-6xl md:text-8xl font-extrabold mb-4 text-white uppercase" style={{ textShadow: '0 0 10px rgba(0,255,0,0.7), 0 0 20px rgba(0,255,0,0.5)' }}>
          ShadowTrace
        </h1>
        
        <GlitchLine />

        <p className="text-xl md:text-2xl mb-8 text-green-300">
           Secure Global Asset Monitoring and Remote Command Execution.
        </p>
        
        <Link 
          href="/register" 
          className="inline-block text-lg px-8 py-3 bg-green-600 text-gray-950 font-bold rounded-lg hover:bg-green-500 transition-colors duration-300 shadow-xl shadow-green-500/50 uppercase tracking-widest"
        >
          Initiate Trace Protocol
        </Link>
        
      </div>
    </section>
  );
}