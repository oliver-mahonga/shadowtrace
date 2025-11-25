"use client";

export default function Topbar() {
  return (
    <div className="w-full h-16 border-b border-green-500/20 bg-black/30 backdrop-blur-md flex items-center justify-between px-6">
      <h2 className="text-green-300 text-lg font-semibold tracking-wide">
        Control Panel
      </h2>

      <div className="flex items-center gap-4">
        <input
          className="bg-black/50 border border-green-500/20 rounded-md px-3 py-1 text-sm text-gray-300 focus:outline-none focus:ring-1 focus:ring-green-400"
          placeholder="Search..."
        />

        <img
          src="/avatar.png"
          alt="User"
          className="w-10 h-10 rounded-full border border-green-500/30"
        />
      </div>
    </div>
  );
}
