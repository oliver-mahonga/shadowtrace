"use client";

import Link from "next/link";
import { motion } from "framer-motion";

interface DeviceActionsProps {
  id: string;
  status: string;
}

export default function DeviceActions({ id, status }: DeviceActionsProps) {
  return (
    <div className="flex flex-col gap-3">
      <Link
        href={`/dashboard/live/${id}`}
        className="bg-green-500 text-black text-sm font-semibold py-2 rounded-md hover:bg-green-400 transition"
      >
        Live Video Feed
      </Link>

      <Link
        href={`/dashboard/control/${id}`}
        className="bg-blue-500/20 text-blue-400 border border-blue-400/30 text-sm py-2 rounded-md hover:bg-blue-400/10 transition"
      >
        Remote Control
      </Link>

      <Link
        href={`/dashboard/map/${id}`}
        className="bg-purple-500/20 text-purple-400 border border-purple-400/30 text-sm py-2 rounded-md hover:bg-purple-400/10 transition"
      >
        GPS Map View
      </Link>

      <button className="bg-yellow-500/20 text-yellow-400 border border-yellow-400/30 text-sm py-2 rounded-md hover:bg-yellow-400/10 transition">
        Trigger Alert
      </button>

      <button
        disabled={status === "offline"}
        className={`text-sm py-2 rounded-md transition border ${
          status === "offline"
            ? "bg-gray-700 text-gray-500 border-gray-700 cursor-not-allowed"
            : "bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-400/10"
        }`}
      >
        Disable Device
      </button>

      <button className="text-sm py-2 rounded-md transition bg-red-500 text-white font-bold hover:bg-red-600">
        Delete Device
      </button>
    </div>
  );
}
