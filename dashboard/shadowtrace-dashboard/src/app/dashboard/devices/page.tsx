"use client";

import { motion } from "framer-motion";
import DeviceCard from "../components/devices/DeviceCard";
// import DeviceCard from "@/components/devices/DeviceCard";

export default function DevicesPage() {
  // TEMP MOCK DATA — replace with real backend API later
  const devices = [
  {
    id: "1",
    name: "Ollie's Pixel 7",
    battery: 87,
    lastOnline: "5 seconds ago",
    network: "5G",
    location: { lat: -1.2921, lng: 36.8219 },
    accuracy: 4.2,
    status: "online" as const,
    distance: "3.2 km",
    movement: "North-East",
    riskScore: 22,
  },
  {
    id: "2",
    name: "Work Phone A52",
    battery: 41,
    lastOnline: "2 minutes ago",
    network: "LTE",
    location: { lat: -1.325, lng: 36.789 },
    accuracy: 10,
    status: "offline" as const,
    distance: "6.1 km",
    movement: "Unknown",
    riskScore: 68,
  },
] as const;


  return (
    <main className="min-h-screen p-10 bg-black text-white">
      <h1 className="text-4xl font-bold text-green-400 mb-10 tracking-wide">
        Connected Devices
      </h1>

      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        {devices.map((device, index) => (
          <motion.div
            key={device.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <DeviceCard device={device} />
          </motion.div>
        ))}
      </motion.div>
    </main>
  );
}
