"use client";

import { motion } from "framer-motion";

export default function DashboardHome() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-green-300 mb-6">
        Dashboard Overview
      </h1>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { title: "Active Devices", value: "8" },
          { title: "Alerts Today", value: "3" },
          { title: "Live Feeds", value: "2" },
        ].map((card, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
            className="p-6 border border-green-500/20 rounded-xl bg-black/40 backdrop-blur-lg shadow-lg"
          >
            <h2 className="text-xl font-semibold text-green-400">
              {card.title}
            </h2>
            <p className="text-4xl mt-3 font-bold">{card.value}</p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
