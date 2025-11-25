"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";

interface DeviceLivePageProps {
  params: { id: string };
}

export default function DeviceLivePage({ params }: DeviceLivePageProps) {
  const deviceId = params.id;

  const [isRecording, setIsRecording] = useState(false);

  const handleSnapshot = () => {
    alert("Snapshot taken (frontend simulation)");
  };

  const handleRecordToggle = () => {
    setIsRecording(prev => !prev);
    alert(isRecording ? "Recording stopped" : "Recording started");
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold text-green-400 mb-6">
        Live Video Feed — Device #{deviceId}
      </h1>

      <div className="relative w-full max-w-5xl aspect-video bg-zinc-900 border border-green-500 rounded-lg overflow-hidden shadow-lg">
        {/* Simulated video feed */}
        <video
          src="https://www.w3schools.com/html/mov_bbb.mp4"
          controls
          autoPlay
          className="w-full h-full object-cover"
        />

        {/* Overlay device info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute top-4 left-4 bg-black/60 backdrop-blur px-3 py-1 rounded-lg border border-green-400 text-green-300 text-sm font-medium"
        >
          Battery: 87% | Status: Online | Network: 5G
        </motion.div>
      </div>

      {/* Action Buttons */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex gap-4 mt-6"
      >
        <button
          onClick={handleSnapshot}
          className="px-6 py-2 rounded-lg border border-green-400 hover:bg-green-400/10 transition font-medium"
        >
          📸 Snapshot
        </button>

        <button
          onClick={handleRecordToggle}
          className={`px-6 py-2 rounded-lg border border-green-400 transition font-medium ${
            isRecording ? "bg-red-600/20" : "hover:bg-green-400/10"
          }`}
        >
          {isRecording ? "⏹ Stop Recording" : "⏺ Start Recording"}
        </button>

        <Link
          href={`/dashboard/devices/${deviceId}/map`}
          className="px-6 py-2 rounded-lg border border-green-400 hover:bg-green-400/10 transition font-medium"
        >
          📍 GPS Map
        </Link>
      </motion.div>
    </main>
  );
}
