import { NavLink } from "react-router-dom";
import { Activity, GraduationCap, LineChart } from "lucide-react";

const linkClass = ({ isActive }) =>
  `flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
    isActive
      ? "bg-brand-600 text-white shadow-sm"
      : "text-slate-600 hover:bg-slate-100"
  }`;

export default function Navbar() {
  return (
    <header className="sticky top-0 z-10 border-b bg-white/80 backdrop-blur">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-lg text-slate-900">
          <span className="w-8 h-8 rounded-lg bg-brand-600 text-white flex items-center justify-center">
            <Activity size={18} />
          </span>
          CampusPulse
        </div>
        <nav className="flex gap-1">
          <NavLink to="/" end className={linkClass}>Home</NavLink>
          <NavLink to="/personalised-learning" className={linkClass}>
            <GraduationCap size={16} /> Personalised Learning
          </NavLink>
          <NavLink to="/academic-performance" className={linkClass}>
            <LineChart size={16} /> Academic Performance
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
