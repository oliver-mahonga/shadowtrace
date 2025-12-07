// components/dashboard/CommandPanel.tsx
'use client';

import { useState } from 'react';
import DashboardPanel from './DashboardPanel';
import { DeviceOut } from '@/types/schemas'; // Import the assumed type

interface CommandPanelProps {
  selectedDevice: DeviceOut | null;
}

// Define available actions for the dropdown
const AVAILABLE_ACTIONS = [
    { value: 'SOUND_SIREN', label: 'SOUND SIREN (Acoustic Alert)' },
    { value: 'LOCK', label: 'LOCK DEVICE (Security Protocol)' },
    { value: 'GET_IMAGE', label: 'CAPTURE IMAGE (Evidence)' },
    // Add other actions (WIPE, etc.) later
];

export default function CommandPanel({ selectedDevice }: CommandPanelProps) {
  const [action, setAction] = useState(AVAILABLE_ACTIONS[0].value);
  const [isSending, setIsSending] = useState(false);
  const [commandLog, setCommandLog] = useState<string[]>([]);

  const handleSendCommand = async () => {
    if (!selectedDevice) {
      setCommandLog(prev => ['// ERROR: No target device selected.'] + prev);
      return;
    }
    
    setIsSending(true);
    setCommandLog(prev => [`// ATTEMPTING: Sending '${action}' to ${selectedDevice.display_name}...`] + prev);

    const token = localStorage.getItem('access_token');
    const deviceId = selectedDevice.id;

    try {
      const response = await fetch(`/api/v1/actions/${deviceId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: action,
          params: {}, // Can be extended for actions needing parameters
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Command dispatch failed.');
      }
      
      const logMessage = `// OK: CMD ID ${data.command_id.substring(0, 8)} | Action: ${data.action} | Status: ${data.status}`;
      setCommandLog(prev => [logMessage] + prev);

    } catch (err: any) {
      setCommandLog(prev => [` CRITICAL ERROR: ${err.message}`] + prev);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <DashboardPanel title="Command Console" className="w-80 min-w-[20rem]">
      
      {/* Command Input Section */}
      <div className="pb-4 border-b border-green-700/50 mb-4">
        <label className="block text-xs uppercase tracking-widest mb-1 text-green-300">
          Target: {selectedDevice ? selectedDevice.display_name : '--- SELECT DEVICE ---'}
        </label>
        
        <select 
          value={action}
          onChange={(e) => setAction(e.target.value)}
          disabled={!selectedDevice || isSending}
          className="w-full mb-3 px-3 py-2 bg-gray-800 border border-green-700/70 rounded-md focus:ring-green-500 text-sm"
        >
          {AVAILABLE_ACTIONS.map(a => (
            <option key={a.value} value={a.value}>{a.label}</option>
          ))}
        </select>
        
        <button
          onClick={handleSendCommand}
          disabled={!selectedDevice || isSending}
          className="w-full py-2 bg-red-700/80 text-white font-bold rounded-md hover:bg-red-600 transition-colors duration-200 
                     shadow-lg shadow-red-900/50 uppercase tracking-widest disabled:opacity-50 disabled:bg-gray-700"
        >
          {isSending ? '// DISPATCHING...' : '// SEND REMOTE ACTION'}
        </button>
      </div>

      {/* Command Log */}
      <div>
        <h3 className="text-xs uppercase tracking-widest mb-2 text-green-500">
           ACTION LOG
        </h3>
        <div className="h-64 overflow-y-auto border border-green-900 bg-gray-950 p-2 text-xs">
          {commandLog.map((log, index) => (
            <div key={index} className={log.startsWith('// ERROR') ? 'text-red-400' : 'text-green-400'}>
              <span className="text-green-600 mr-1">[{new Date().toLocaleTimeString('en-US', {hour12: false})}]</span> 
              {log}
            </div>
          ))}
          {!commandLog.length && <p className="text-gray-600">Awaiting user commands...</p>}
        </div>
      </div>
    </DashboardPanel>
  );
}