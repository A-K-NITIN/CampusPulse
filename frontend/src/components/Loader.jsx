export default function Loader({ label = "Loading..." }) {
  return (
    <div className="flex items-center gap-2 text-slate-500 text-sm py-6">
      <span className="w-4 h-4 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
      {label}
    </div>
  );
}
