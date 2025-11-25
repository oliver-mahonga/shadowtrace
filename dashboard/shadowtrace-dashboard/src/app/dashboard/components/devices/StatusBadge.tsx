export default function StatusBadge({ status }: { status: string }) {
  return (
    <span
      className={`px-3 py-1 text-xs font-bold rounded-full ${
        status === "online"
          ? "bg-green-500/20 text-green-400 border border-green-500/40"
          : "bg-red-500/20 text-red-400 border border-red-500/40"
      }`}
    >
      {status.toUpperCase()}
    </span>
  );
}
