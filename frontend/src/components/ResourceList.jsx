export default function ResourceList({ resources }) {
  return (
    <div className="space-y-5">
      {Object.entries(resources).map(([subject, topics]) => (
        <div key={subject}>
          <h4 className="font-medium text-sm text-slate-500 mb-2">{subject}</h4>
          <div className="space-y-2">
            {Object.entries(topics).map(([topic, matches]) => (
              <div key={topic} className="bg-white border border-slate-200 rounded-lg p-4 shadow-card">
                <p className="text-sm font-semibold text-slate-800">{topic}</p>
                {matches.map((m, i) => (
                  <p key={i} className="text-xs text-slate-500 mt-1.5">
                    <span className="inline-block bg-slate-100 text-slate-600 rounded px-1.5 py-0.5 mr-1.5 uppercase tracking-wide">
                      {m.metadata.type}
                    </span>
                    {m.content}
                  </p>
                ))}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
