"use client";

import { motion } from "framer-motion";
import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-black text-white relative overflow-hidden font-sans">
      {/* Hacker grid background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,255,180,0.07),transparent_60%)] pointer-events-none" />
      <div className="absolute inset-0 bg-[linear-gradient(90deg,rgba(0,255,120,0.05)_1px,transparent_1px),linear-gradient(rgba(0,255,120,0.05)_1px,transparent_1px)] bg-[size:40px_40px]" />

      {/* NAVBAR */}
      <motion.nav
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between px-10 py-6 border-b border-green-500/20"
      >
        <h1 className="text-2xl font-bold tracking-wider text-green-400">
          SHADOWTRACE<span className="text-gray-500">.AI</span>
        </h1>

        <div className="flex items-center gap-8 text-sm">
          <Link className="hover:text-green-400 transition" href="#features">
            Features
          </Link>

          <Link className="hover:text-green-400 transition" href="#how">
            How it Works
          </Link>

          <Link className="hover:text-green-400 transition" href="#contact">
            Contact
          </Link>

          <Link
            href="/dashboard"
            className="px-5 py-2 bg-green-500 text-black font-semibold rounded-md hover:bg-green-400 transition"
          >
            Launch App
          </Link>
        </div>
      </motion.nav>

      {/* HERO SECTION */}
      <section className="px-10 pt-28">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl"
        >
          <h2 className="text-6xl font-extrabold leading-tight text-green-300 drop-shadow-[0_0_15px_rgba(0,255,180,0.4)]">
            Track Anything.
            <br />
            Anywhere.
            <br />
            In Real-Time.
          </h2>

          <p className="mt-6 text-lg text-gray-300">
            ShadowTrace uses AI + spatial intelligence to give you live
            positioning, control, and surveillance over your devices. A system
            built for precision, power, and full remote control.
          </p>

          <div className="mt-10 flex gap-6">
            <Link
              href="/dashboard"
              className="px-6 py-3 bg-green-500 text-black font-semibold rounded-md hover:bg-green-400 transition"
            >
              Go to Dashboard
            </Link>

            <a
              href="#features"
              className="px-6 py-3 border border-green-500 text-green-400 rounded-md hover:bg-green-500 hover:text-black transition"
            >
              Explore Features
            </a>
          </div>
        </motion.div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="px-10 mt-40">
        <h3 className="text-4xl font-bold text-green-300 mb-10">Core Features</h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {[
            {
              title: "Live Spatial Tracking",
              desc: "Real-time GPS position updates, direction, trails, and geo-fencing.",
            },
            {
              title: "AI Camera Feeds",
              desc: "Live video stitched with object detection and remote movement.",
            },
            {
              title: "Remote Device Control",
              desc: "Send commands to move cameras, drones, and robots.",
            },
          ].map((f, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.2 }}
              className="p-8 border border-green-500/20 rounded-xl bg-black/40 backdrop-blur-sm hover:border-green-400/40 transition"
            >
              <h4 className="text-xl font-semibold text-green-400">
                {f.title}
              </h4>
              <p className="mt-3 text-gray-300">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </main>
  );
}
