import { useState } from "react";
import { Search } from "lucide-react";
import Loader from "../components/Loader.jsx";
import RecoveryPlanCard from "../components/RecoveryPlanCard.jsx";
import IntensityGrid from "../components/IntensityGrid.jsx";
import ResourceList from "../components/ResourceList.jsx";
import RevisionList from "../components/RevisionList.jsx";
import RiskBadge from "../components/RiskBadge.jsx";
import {
  fetchRiskProfile,
  fetchRecoveryPlan,
  fetchIntensity,
  fetchResources,
  fetchRevisionPlan,
} from "../api/client.js";

export default function PersonalisedLearning() {
  const [rollNo, setRollNo] = useState("21CS003");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  async function handleLookup(e) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const [risk, plan, intensity, resources, revision] = await Promise.all([
        fetchRiskProfile(rollNo),
        fetchRecoveryPlan(rollNo),
        fetchIntensity(rollNo),
        fetchResources(rollNo),
        fetchRevisionPlan(rollNo),
      ]);
      setData({ risk, plan, intensity, resources, revision });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Personalised Learning</h1>
        <p className="text-slate-500 text-sm mt-1">Look up a student to view their catch-up plan.</p>
      </div>

      <form onSubmit={handleLookup} className="flex gap-2 max-w-md">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
            placeholder="Roll number, e.g. 21CS003"
            className="w-full border border-slate-200 rounded-lg pl-9 pr-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
          />
        </div>
        <button
          type="submit"
          className="bg-brand-600 text-white px-5 py-2.5 rounded-lg text-sm font-medium hover:bg-brand-700 transition-colors shadow-sm"
        >
          Look up
        </button>
      </form>

      {loading && <Loader label="Running pipeline..." />}
      {error && <p className="text-red-600 text-sm">{error}</p>}

      {data && (
        <div className="space-y-10">
          <section>
            <h2 className="font-semibold text-slate-800 mb-3">Risk profile</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.risk).map(([subject, v]) => (
                <div key={subject} className="bg-white border border-slate-200 rounded-lg px-3 py-2 flex items-center gap-2 text-sm shadow-card">
                  <span className="font-medium text-slate-700">{subject}</span>
                  <RiskBadge level={v.risk} />
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="font-semibold text-slate-800 mb-3">Recovery plan</h2>
            <div className="grid sm:grid-cols-2 gap-4">
              {Object.entries(data.plan).map(([subject, d]) => (
                <RecoveryPlanCard key={subject} subject={subject} data={d} />
              ))}
            </div>
          </section>

          <section>
            <h2 className="font-semibold text-slate-800 mb-3">Study intensity</h2>
            <IntensityGrid intensity={data.intensity} />
          </section>

          <section>
            <h2 className="font-semibold text-slate-800 mb-3">Recommended resources</h2>
            <ResourceList resources={data.resources} />
          </section>

          <section>
            <h2 className="font-semibold text-slate-800 mb-3">Revision priorities</h2>
            <RevisionList revision={data.revision} />
          </section>
        </div>
      )}
    </div>
  );
}
