"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { LatLngExpression } from "leaflet";

// Dynamic imports with `as any` to avoid TypeScript overload issues
const MapContainer = dynamic(() => import("react-leaflet").then(m => m.MapContainer), { ssr: false }) as any;
const TileLayer = dynamic(() => import("react-leaflet").then(m => m.TileLayer), { ssr: false }) as any;
const Marker = dynamic(() => import("react-leaflet").then(m => m.Marker), { ssr: false }) as any;
const Circle = dynamic(() => import("react-leaflet").then(m => m.Circle), { ssr: false }) as any;
const Polyline = dynamic(() => import("react-leaflet").then(m => m.Polyline), { ssr: false }) as any;
const HeatmapLayer = dynamic(() => import("react-leaflet-heatmap-layer"), { ssr: false }) as any;

interface DeviceMapPageProps {
  params: { id: string };
}

export default function DeviceMapPage({ params }: DeviceMapPageProps) {
  const deviceId = params.id;

  const [position, setPosition] = useState<LatLngExpression>([-1.286389, 36.817223]);
  const [accuracy, setAccuracy] = useState<number>(15);
  const [path, setPath] = useState<LatLngExpression[]>([]);
  const [heatPoints, setHeatPoints] = useState<[number, number, number][]>([]);

  // Simulate live movement
  useEffect(() => {
    const interval = setInterval(() => {
      const newLat = (position as [number, number])[0] + (Math.random() - 0.5) * 0.0008;
      const newLng = (position as [number, number])[1] + (Math.random() - 0.5) * 0.0008;

      setPosition([newLat, newLng]);
      setAccuracy(Math.random() * 20 + 5);
      setPath(prev => [...prev, [newLat, newLng]]);
      setHeatPoints(prev => [...prev, [newLat, newLng, 0.6]]);
    }, 3000);

    return () => clearInterval(interval);
  }, [position]);

  return (
    <main className="h-screen w-full bg-black text-white flex overflow-hidden">
      {/* LEFT: MAP */}
      <div className="w-[70%] h-full relative">
        <MapContainer
          center={position}
          zoom={16}
          style={{ height: "100%", width: "100%" }}
          scrollWheelZoom={true}
        >
          <TileLayer url="https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png" />
          <Circle
            center={position}
            radius={accuracy}
            pathOptions={{ color: "blue", fillColor: "blue", fillOpacity: 0.2 }}
          />
          <Marker position={position} />
          <Polyline positions={path} pathOptions={{ color: "lime" }} />
          <HeatmapLayer
            points={heatPoints}
            longitudeExtractor={p => p[1]}
            latitudeExtractor={p => p[0]}
            intensityExtractor={p => p[2]}
            fitBoundsOnLoad
            fitBoundsOnUpdate
          />
        </MapContainer>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute top-5 left-5 bg-black/60 backdrop-blur px-4 py-2 rounded-lg border border-green-500 text-green-300"
        >
          LIVE TRACKING — Device #{deviceId}
        </motion.div>
      </div>

      {/* RIGHT: SPATIAL DASHBOARD */}
      <div className="w-[30%] h-full p-6 overflow-y-scroll bg-black/80 border-l border-green-500">
        <h2 className="text-2xl font-bold text-green-400 mb-4">Spatial Dashboard</h2>

        <div className="space-y-5">
          <section className="p-4 bg-zinc-900 rounded-xl border border-zinc-700">
            <h3 className="text-lg font-semibold text-green-300">Current Location</h3>
            <p className="text-sm mt-2">
              Latitude: {(position as [number, number])[0].toFixed(6)} <br />
              Longitude: {(position as [number, number])[1].toFixed(6)} <br />
              Accuracy: {accuracy.toFixed(1)}m
            </p>
          </section>

          <section className="p-4 bg-zinc-900 rounded-xl border border-zinc-700">
            <h3 className="text-lg font-semibold text-green-300">Movement Path</h3>
            <p className="text-sm mt-2">Points tracked: {path.length}</p>
          </section>

          <section className="p-4 bg-zinc-900 rounded-xl border border-zinc-700">
            <h3 className="text-lg font-semibold text-green-300">Heat Map Density</h3>
            <p className="text-sm mt-2">Heat points: {heatPoints.length}</p>
          </section>

          <section className="p-4 bg-zinc-900 rounded-xl border border-zinc-700">
            <h3 className="text-lg font-semibold text-green-300">Analytics</h3>
            <ul className="text-sm mt-2 list-disc pl-4 space-y-1">
              <li>Distance Travelled (PostGIS)</li>
              <li>Speed Calculation</li>
              <li>Stay Points</li>
              <li>Geo-Fence Alerts</li>
              <li>Risk Score</li>
            </ul>
          </section>
        </div>
      </div>
    </main>
  );
}
