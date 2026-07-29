import { Link } from "react-router-dom";
import { GraduationCap, LineChart, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <div className="space-y-12">
      <section className="text-center max-w-2xl mx-auto py-10">
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-slate-900">
          Campus<span className="text-brand-600">Pulse</span>
        </h1>
        <p className="mt-4 text-slate-500 text-lg">
          Two agent systems, one campus. One you interact with — the other just quietly does its job.
        </p>
      </section>

      <div className="grid sm:grid-cols-2 gap-5">
        <Link
          to="/personalised-learning"
          className="group block p-6 rounded-2xl border border-slate-200 bg-white shadow-card hover:shadow-cardHover transition-all"
        >
          <div className="w-10 h-10 rounded-lg bg-brand-50 text-brand-600 flex items-center justify-center mb-4">
            <GraduationCap size={20} />
          </div>
          <h2 className="font-semibold text-lg text-slate-900">Personalised Learning Agent</h2>
          <p className="text-sm text-slate-500 mt-2 leading-relaxed">
            Look up a student, see their risk profile, recovery plan, study
            timetable, resources, and revision priorities.
          </p>
          <span className="inline-flex items-center gap-1 text-brand-600 text-sm font-medium mt-4 group-hover:gap-2 transition-all">
            Open dashboard <ArrowRight size={14} />
          </span>
        </Link>

        <Link
          to="/academic-performance"
          className="group block p-6 rounded-2xl border border-slate-200 bg-white shadow-card hover:shadow-cardHover transition-all"
        >
          <div className="w-10 h-10 rounded-lg bg-brand-50 text-brand-600 flex items-center justify-center mb-4">
            <LineChart size={20} />
          </div>
          <h2 className="font-semibold text-lg text-slate-900">Academic Performance Agent</h2>
          <p className="text-sm text-slate-500 mt-2 leading-relaxed">
            Fully automated — runs on a schedule and emails attendance,
            deadline, faculty, and HOD alerts. No dashboard needed.
          </p>
          <span className="inline-flex items-center gap-1 text-brand-600 text-sm font-medium mt-4 group-hover:gap-2 transition-all">
            See how it runs <ArrowRight size={14} />
          </span>
        </Link>
      </div>
    </div>
  );
}
