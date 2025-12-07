// components/dashboard/DashboardPanel.tsx

import React from 'react';

interface DashboardPanelProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export default function DashboardPanel({ title, children, className = '' }: DashboardPanelProps) {
  return (
    <div 
      className={`h-full overflow-hidden flex flex-col 
                  bg-gray-900/70 border border-green-700/50 rounded-lg 
                  shadow-xl shadow-green-900/50 transition-all duration-300 ${className}`}
    >
      {/* Title Bar with Hacking Aesthetic */}
      <div className="px-4 py-3 border-b border-green-700 bg-gray-800/80">
        <h2 className="text-sm font-bold uppercase tracking-wider text-green-300">
          &gt; {title}
        </h2>
      </div>
      
      {/* Content Area */}
      <div className="flex-1 p-3 overflow-y-auto text-sm scrollbar-thin scrollbar-thumb-green-900 scrollbar-track-gray-950">
        {children}
      </div>
    </div>
  );
}