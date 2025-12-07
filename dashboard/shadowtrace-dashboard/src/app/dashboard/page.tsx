// app/dashboard/page.tsx
'use client';

import { useState } from 'react';
import Header from '../../../components/Header';
import DeviceSidebar from '../../../components/dashboard/DeviceSidebar';
import MainMapView from '../../../components/dashboard/MainMapView';
import CommandPanel from '../../../components/dashboard/CommandPanel';
// import Header from '../../components/Header';
// import DeviceSidebar from '../../components/dashboard/DeviceSidebar';
// import MainMapView from '../../components/dashboard/MainMapView';
// import CommandPanel from '../../components/dashboard/CommandPanel';
// import { DeviceOut } from '@/types/schemas'; // Assuming you create this type file

// Define a simple type for the device data we'll use in the frontend
// NOTE: Create a file at src/types/schemas.ts or similar, and add the structure below:
// export interface DeviceOut {
//     id: string; // uuid string
//     unique_device_id: string;
//     display_name: string | null;
//     status: string | null; // e.g., 'online', 'offline'
//     last_active: string | null; // datetime string
// }


export default function Dashboard() {
  const [selectedDevice, setSelectedDevice] = useState<DeviceOut | null>(null);

  return (
    <div className="min-h-screen bg-gray-950 text-green-400 font-mono flex flex-col">
      <Header />
      
      {/* Main Grid Layout */}
      <main className="flex flex-1 pt-16 p-4 space-x-4">
        
        {/* LEFT COLUMN: Device List & Status */}
        <DeviceSidebar 
          selectedDevice={selectedDevice} 
          onDeviceSelect={setSelectedDevice} 
        />

        {/* CENTER COLUMN: Map & Trajectory */}
        <div className="flex-1 min-w-0">
          <MainMapView selectedDevice={selectedDevice} />
        </div>

        {/* RIGHT COLUMN: Commands & Log */}
        <CommandPanel selectedDevice={selectedDevice} />

      </main>
      
      {/* Status Overlay/Footer (Optional) */}
      <footer className="p-2 text-xs text-center border-t border-green-700/50">
         SYSTEM STATUS: TRACE PROTOCOL ACTIVE // USER: AUTHENTICATED
      </footer>
    </div>
  );
}