export default function RiskBadge({ score }: { score: number }) {
  let color = "text-green-400 border-green-500/40 bg-green-500/10";

  if (score >= 70)
    color = "text-red-400 border-red-500/40 bg-red-500/10";
  else if (score >= 30)
    color = "text-yellow-400 border-yellow-500/40 bg-yellow-500/10";

  return (
    <span
      className={`px-3 py-1 text-xs font-semibold border rounded-full ${color}`}
    >
      Risk Score: {score}
    </span>
  );
}
