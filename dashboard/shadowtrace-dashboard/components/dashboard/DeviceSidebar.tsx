// components/dashboard/DeviceSidebar.tsx
'use client';

import { useEffect, useState } from 'react';
import DashboardPanel from './DashboardPanel';
import { DeviceOut } from '@/types/schemas'; // Import the assumed type

interface DeviceSidebarProps {
  selectedDevice: DeviceOut | null;
  onDeviceSelect: (device: DeviceOut) => void;
}

export default function DeviceSidebar({ selectedDevice, onDeviceSelect }: DeviceSidebarProps) {
  const [devices, setDevices] = useState<DeviceOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDevices = async () => {
      setLoading(true);
      setError('');
      const token = localStorage.getItem('access_token');
      if (!token) {
        setError('Authorization token missing.');
        setLoading(false);
        return;
      }

      try {
        const response = await fetch('/api/v1/devices/', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch devices. Token may be expired.');
        }

        const data: DeviceOut[] = await response.json();
        setDevices(data);
        if (data.length > 0 && !selectedDevice) {
          onDeviceSelect(data[0]); // Auto-select the first device
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDevices();
    
    // Optional: Refresh device list periodically
    const intervalId = setInterval(fetchDevices, 60000); 
    return () => clearInterval(intervalId);

  }, [onDeviceSelect, selectedDevice]);

  const getStatusColor = (status: string | null) => {
    switch (status) {
      case 'active': return 'text-green-500';
      case 'offline': return 'text-red-500';
      default: return 'text-yellow-500';
    }
  };

  return (
    <DashboardPanel title="Target Systems" className="w-64 min-w-[16rem]">
      {loading && <p className="animate-pulse"> SCANNING FOR ASSETS...</p>}
      {error && <p className="text-red-500"> ERROR: {error}</p>}

      <ul className="space-y-2">
        {devices.map((device) => (
          <li 
            key={device.id}
            onClick={() => onDeviceSelect(device)}
            className={`p-2 cursor-pointer border-l-4 transition-all duration-150 
              ${selectedDevice?.id === device.id 
                ? 'bg-green-800/30 border-green-500 shadow-lg shadow-green-900/50' 
                : 'bg-gray-800/30 border-green-900 hover:bg-green-900/20'
              }`}
          >
            <div className="font-bold">{device.display_name || device.unique_device_id}</div>
            <div className={`text-xs ${getStatusColor(device.status)}`}>
              {device.status ? `Status: ${device.status.toUpperCase()}` : 'Status: UNKNOWN'}
            </div>
          </li>
        ))}
      </ul>
    </DashboardPanel>
  );
}