"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ReactNode } from "react";

interface NavItemProps {
  icon: ReactNode;
  label: string;
  href: string;
}

export default function NavItem({ icon, label, href }: NavItemProps) {
  return (
    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.97 }}>
      <Link
        href={href}
        className="flex items-center gap-3 px-4 py-3 text-gray-300 hover:text-green-400 hover:bg-green-400/10 rounded-lg transition"
      >
        <span className="text-xl">{icon}</span>
        <span className="text-sm font-medium">{label}</span>
      </Link>
    </motion.div>
  );
}
