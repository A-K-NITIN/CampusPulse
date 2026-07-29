export default function RevisionList({ revision }) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-card space-y-4">
      <p className="text-sm text-slate-600 leading-relaxed">{revision.revision_text}</p>
      <ol className="space-y-2">
        {revision.backlog
          .sort((a, b) => a.risk_rank - b.risk_rank)
          .map((item, i) => (
            <li key={`${item.subject}-${item.topic}`} className="flex items-center justify-between text-sm border-t border-slate-100 pt-2 first:border-0 first:pt-0">
              <span className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-brand-50 text-brand-700 text-xs font-semibold flex items-center justify-center">{i + 1}</span>
                {item.subject} — {item.topic}
              </span>
              <span className="text-slate-400 text-xs">exam {item.exam_date}</span>
            </li>
          ))}
      </ol>
    </div>
  );
}
