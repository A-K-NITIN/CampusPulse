export default function IntensityGrid({ intensity }) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-card">
      <table className="w-full text-sm">
        <thead className="bg-slate-50 text-slate-500 text-left">
          <tr>
            <th className="px-4 py-3 font-medium">Subject</th>
            <th className="px-4 py-3 font-medium">Hours/week</th>
            <th className="px-4 py-3 font-medium">Days/week</th>
            <th className="px-4 py-3 font-medium">Session length</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {Object.entries(intensity).map(([subject, v]) => (
            <tr key={subject} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-medium text-slate-800">{subject}</td>
              <td className="px-4 py-3">{v.hours_per_week}h</td>
              <td className="px-4 py-3">{v.days_per_week}</td>
              <td className="px-4 py-3">{v.session_minutes} min</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
