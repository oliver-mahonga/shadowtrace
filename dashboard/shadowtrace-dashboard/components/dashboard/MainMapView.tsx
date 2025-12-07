// components/dashboard/MainMapView.tsx
'use client';

import { useEffect, useState } from 'react';
import DashboardPanel from './DashboardPanel';
import { DeviceOut } from '@/types/schemas'; // Import the assumed type
// NOTE: For a real map, you would import leaflet or react-map-gl here

interface MainMapViewProps {
  selectedDevice: DeviceOut | null;
}

interface LocationData {
    lat: number;
    lon: number;
    accuracy: number | null;
    speed: number | null;
    recorded_at: string;
}

export default function MainMapView({ selectedDevice }: MainMapViewProps) {
  const [location, setLocation] = useState<LocationData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Function to fetch the latest location
  const fetchLatestLocation = async () => {
    if (!selectedDevice) return;
    setLoading(true);
    setError('');

    const token = localStorage.getItem('access_token');
    if (!token) {
        setError('Auth missing.');
        setLoading(false);
        return;
    }

    try {
        const response = await fetch(`/api/v1/locations/${selectedDevice.id}/last`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        const data = await response.json();
        
        if (!response.ok || !data.location) {
            throw new Error(data.message || 'No recent location data.');
        }

        setLocation(data.location as LocationData);
    } catch (err: any) {
        setError(err.message);
        setLocation(null);
    } finally {
        setLoading(false);
    }
  };

  // Effect to re-fetch when device changes and poll periodically
  useEffect(() => {
    setLocation(null);
    setError('');
    
    // Fetch immediately when a device is selected
    if (selectedDevice) {
        fetchLatestLocation();
    }

    // Set up polling for location updates (e.g., every 15 seconds)
    const intervalId = setInterval(fetchLatestLocation, 15000); 
    
    // Cleanup: clear interval when component unmounts or device changes
    return () => clearInterval(intervalId);

  }, [selectedDevice]);


  const renderMapPlaceholder = () => (
    <div className="w-full h-full bg-gray-950/90 flex flex-col items-center justify-center p-8 border border-green-700/30">
        <div className="text-xl text-green-700 animate-pulse mb-4">
             MAP ENGINE INITIATING...
        </div>
        <div className="w-40 h-1 bg-green-900 rounded-full overflow-hidden">
            <div className={`h-full bg-green-500 animate-slide-in`} style={{width: '60%'}}></div>
        </div>
        <p className="text-xs mt-4 text-gray-500">
            [NOTE: Real-time map rendering requires Leaflet/Mapbox setup.]
        </p>
    </div>
  );

  return (
    <DashboardPanel title={`Tracking Target: ${selectedDevice ? selectedDevice.display_name : 'No Target Selected'}`} className="h-[calc(100vh-80px)]">
      
      {/* The main map area */}
      <div className="h-4/5 w-full border border-green-700/50 mb-3 relative">
        {loading && <div className="absolute inset-0 bg-gray-900/80 flex items-center justify-center z-10 animate-pulse">// LOADING LOCATION DATA...</div>}
        {error && <div className="absolute inset-0 bg-red-900/20 text-red-500 flex items-center justify-center z-10">// ERROR: {error}</div>}
        
        {renderMapPlaceholder()}
      </div>

      {/* Location Details/Telemetry */}
      <div className="h-1/5 grid grid-cols-2 gap-3 border-t border-green-700/50 pt-3">
        <div className="space-y-1">
            <h3 className="text-xs uppercase tracking-widest text-green-500"> LATEST TELEMETRY</h3>
            <p className="text-sm">LAT: {location?.lat.toFixed(6) || '---'}</p>
            <p className="text-sm">LON: {location?.lon.toFixed(6) || '---'}</p>
        </div>
        <div className="space-y-1 border-l border-green-700/50 pl-3">
            <h3 className="text-xs uppercase tracking-widest text-green-500"> METRICS</h3>
            <p className="text-sm">SPEED: {(location?.speed || 0).toFixed(2)} m/s</p>
            <p className="text-sm">ACCURACY: {(location?.accuracy || 0).toFixed(2)} m</p>
            <p className="text-sm text-gray-500">LAST SYNC: {location?.recorded_at ? new Date(location.recorded_at).toLocaleTimeString() : '---'}</p>
        </div>
      </div>
      
    </DashboardPanel>
  );
}