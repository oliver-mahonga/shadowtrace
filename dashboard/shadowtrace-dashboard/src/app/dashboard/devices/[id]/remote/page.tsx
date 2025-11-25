"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { BellRing, Smartphone, Unlock, Camera } from "lucide-react";

interface DeviceRemotePageProps {
  params: { id: string };
}

export default function DeviceRemotePage({ params }: DeviceRemotePageProps) {
  const deviceId = params.id;
  const [status, setStatus] = useState({
    battery: 87,
    network: "5G",
    online: true,
  });

  const handleAction = (action: string) => {
    switch (action) {
      case "ring":
        alert(`Device ${deviceId} is ringing`);
        break;
      case "vibrate":
        alert(`Device ${deviceId} is vibrating`);
        break;
      case "unlock":
        alert(`Device ${deviceId} unlocked`);
        break;
      case "screenshot":
        alert(`Screenshot taken for Device ${deviceId}`);
        break;
      default:
        break;
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-green-400 mb-6">
        Remote Control — Device #{deviceId}
      </h1>

      {/* Device Status Panel */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-3xl bg-zinc-900 border border-green-400 rounded-lg p-4 flex justify-between mb-8"
      >
        <div className="text-green-300">
          <p>Battery: {status.battery}%</p>
          <p>Network: {status.network}</p>
          <p>Status: {status.online ? "Online" : "Offline"}</p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() => handleAction("ring")}
            className="flex items-center gap-2 px-4 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition"
          >
            <BellRing size={20} /> Ring
          </button>
          <button
            onClick={() => handleAction("vibrate")}
            className="flex items-center gap-2 px-4 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition"
          >
            <Smartphone size={20} /> Vibrate
          </button>
          <button
            onClick={() => handleAction("unlock")}
            className="flex items-center gap-2 px-4 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition"
          >
            <Unlock size={20} /> Unlock
          </button>
          <button
            onClick={() => handleAction("screenshot")}
            className="flex items-center gap-2 px-4 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition"
          >
            <Camera size={20} /> Screenshot
          </button>
        </div>
      </motion.div>

      {/* Navigation Links */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-3xl flex gap-4 justify-between"
      >
        <Link
          href={`/dashboard/devices/${deviceId}/live`}
          className="flex items-center justify-center gap-2 px-6 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition w-full"
        >
          <Camera size={18} /> Live Video
        </Link>
        <Link
          href={`/dashboard/devices/${deviceId}/map`}
          className="flex items-center justify-center gap-2 px-6 py-2 border border-green-400 rounded-lg hover:bg-green-400/10 transition w-full"
        >
          <BellRing size={18} /> GPS Map
        </Link>
      </motion.div>
    </main>
  );
}
