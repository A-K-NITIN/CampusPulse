import { Clock } from "lucide-react";

const jobs = [
  { time: "8:00 AM daily", name: "Attendance reminders" },
  { time: "8:30 AM daily", name: "Deadline reminders" },
  { time: "9:00 AM daily", name: "Pre-exam faculty alerts" },
  { time: "9:00 AM Mondays", name: "HOD subject alerts" },
  { time: "10:00 AM Mondays", name: "Hackathon matching" },
];

export default function AcademicPerformance() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Academic Performance Agent</h1>
        <p className="text-slate-500 mt-2 leading-relaxed">
          This agent is inbuilt and self-running — it's triggered by
          <code className="mx-1 px-1.5 py-0.5 bg-slate-100 rounded text-sm">main.py</code>'s
          scheduler, not by a user, so there's no dashboard to build here.
        </p>
      </div>
      <div className="bg-white border border-slate-200 rounded-xl divide-y divide-slate-100 shadow-card">
        {jobs.map((j) => (
          <div key={j.name} className="flex items-center justify-between px-5 py-3.5 text-sm">
            <span className="text-slate-800 font-medium">{j.name}</span>
            <span className="flex items-center gap-1.5 text-slate-400">
              <Clock size={14} /> {j.time}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
