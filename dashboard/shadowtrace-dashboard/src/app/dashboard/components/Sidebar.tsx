"use client";

import NavItem from "./NavItem";
import { FaCamera, FaMapMarkedAlt, FaRobot, FaChartBar, FaVideo, FaCog, FaBell } from "react-icons/fa";

export default function Sidebar() {
  return (
    <div className="h-screen w-64 border-r border-green-500/20 bg-black/40 backdrop-blur-md p-5 flex flex-col">
      <h1 className="text-2xl font-bold mb-10 tracking-wide text-green-400">
        SHADOWTRACE
      </h1>

      <div className="flex-1 flex flex-col gap-3">
        <NavItem icon={<FaChartBar />} label="Dashboard" href="/dashboard" />
        <NavItem icon={<FaCamera />} label="Devices" href="/dashboard/devices" />
        <NavItem icon={<FaVideo />} label="Live Feed" href="/dashboard/live" />
        <NavItem icon={<FaRobot />} label="Remote Control" href="/dashboard/control" />
        <NavItem icon={<FaMapMarkedAlt />} label="Map" href="/dashboard/map" />
        <NavItem icon={<FaBell />} label="Alerts" href="/dashboard/alerts" />
      </div>

      <div className="mt-auto">
        <NavItem icon={<FaCog />} label="Settings" href="/dashboard/settings" />
      </div>
    </div>
  );
}
