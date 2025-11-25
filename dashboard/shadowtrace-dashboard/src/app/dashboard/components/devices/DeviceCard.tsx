"use client";

import { motion } from "framer-motion";
import StatusBadge from "./StatusBadge";
import RiskBadge from "./RiskBadge";
import DeviceActions from "./DeviceActions";

interface DeviceCardProps {
  device: {
    id: string;
    name: string;
    battery: number;
    lastOnline: string;
    network: string;
    location: { lat: number; lng: number };
    accuracy: number;
    status: "online" | "offline";
    distance: string;
    movement: string;
    riskScore: number;
  };
}

export default function DeviceCard({ device }: DeviceCardProps) {
  return (
    <div className="border border-green-500/20 bg-black/30 backdrop-blur-md p-6 rounded-xl hover:border-green-400/40 transition">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold text-green-300">{device.name}</h2>
        <StatusBadge status={device.status} />
      </div>

      <p className="text-gray-400 text-sm mt-2">
        Last online: {device.lastOnline}
      </p>

      {/* Battery + Network */}
      <div className="flex justify-between mt-6 text-gray-300">
        <p>Battery: {device.battery}%</p>
        <p>{device.network}</p>
      </div>

      {/* Location */}
      <div className="mt-4 text-gray-300 text-sm">
        <p>
          GPS: {device.location.lat}, {device.location.lng}
        </p>
        <p>Accuracy: ±{device.accuracy}m</p>
        <p>Movement: {device.movement}</p>
        <p>Distance: {device.distance}</p>
      </div>

      {/* Risk Score */}
      <div className="mt-4">
        <RiskBadge score={device.riskScore} />
      </div>

      {/* Action Buttons */}
      <div className="mt-6">
        <DeviceActions id={device.id} status={device.status} />
      </div>
    </div>
  );
}
