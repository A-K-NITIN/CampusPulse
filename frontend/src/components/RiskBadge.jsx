const styles = {
  high: "bg-red-50 text-red-700 ring-1 ring-red-200",
  medium: "bg-amber-50 text-amber-700 ring-1 ring-amber-200",
  low: "bg-green-50 text-green-700 ring-1 ring-green-200",
};

export default function RiskBadge({ level }) {
  return (
    <span className={`px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wide ${styles[level] || "bg-slate-100 text-slate-600"}`}>
      {level} risk
    </span>
  );
}
