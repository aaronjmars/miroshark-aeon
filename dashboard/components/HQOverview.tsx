import type { Skill, Run } from '../lib/types'
import { DEPARTMENTS } from '../lib/constants'
import { timeAgo } from '../lib/utils'

interface HQOverviewProps {
  skills: Skill[]
  runs: Run[]
  enabledCount: number
  workingCount: number
  onViewRun: (run: Run) => void
}

export function HQOverview({ skills, runs, enabledCount, workingCount, onViewRun }: HQOverviewProps) {
  const departments = new Map<string, Skill[]>()
  skills.forEach(s => { const t = s.tags?.[0] || 'meta'; if (!departments.has(t)) departments.set(t, []); departments.get(t)!.push(s) })

  return (
    <div className="max-w-3xl mx-auto space-y-[var(--space-lg)]">
      {/* Stats */}
      <div className="grid grid-cols-4 gap-[var(--space-sm)]">
        {[
          { label: 'Team Size', value: skills.length, color: '' },
          { label: 'On Duty', value: enabledCount, color: 'text-eva-green' },
          { label: 'Working', value: workingCount, color: 'text-eva-orange' },
          { label: 'Departments', value: departments.size, color: '' },
        ].map(s => (
          <div key={s.label} className="card-hst p-[var(--space-md)]">
            <div className="text-label">{s.label}</div>
            <div className={`font-display text-3xl mt-1 ${s.color}`}>{s.value}</div>
          </div>
        ))}
      </div>

      <div className="warning-stripes" />

      {/* Departments */}
      <div>
        <div className="text-label mb-[var(--space-sm)]">Departments</div>
        <div className="grid grid-cols-2 gap-[var(--space-sm)]">
          {[...departments.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([tag, ts]) => {
            const d = DEPARTMENTS[tag] || DEPARTMENTS.meta; const en = ts.filter(s => s.enabled).length
            return (
              <div key={tag} className="card-hst card-hst-orange p-[var(--space-md)] flex items-center gap-3">
                <div className="w-9 h-9 flex items-center justify-center text-white text-xs font-bold font-mono" style={{ backgroundColor: d.color }}>{d.label.slice(0, 2).toUpperCase()}</div>
                <div><div className="text-sm font-display">{d.label}</div><div className="text-[11px] text-primary-40 font-mono">{ts.length} members &middot; {en} active</div></div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Activity */}
      <div>
        <div className="text-label mb-[var(--space-sm)]">Recent Activity</div>
        <div className="card-hst divide-y divide-[rgba(10,10,10,0.06)]">
          {runs.slice(0, 8).map(run => (
            <button key={run.id} onClick={() => onViewRun(run)}
              className="w-full flex items-center gap-3 px-[var(--space-md)] py-[var(--space-sm)] hover:bg-eva-gray transition-colors text-left">
              <span className={`text-sm ${run.conclusion === 'success' ? 'text-eva-green' : run.conclusion === 'failure' ? 'text-eva-red' : run.status === 'in_progress' ? 'text-eva-orange' : 'text-primary-35'}`}>
                {run.conclusion === 'success' ? '\u2713' : run.conclusion === 'failure' ? '\u2717' : run.status === 'in_progress' ? '\u25cc' : '\u00b7'}
              </span>
              <span className="text-xs text-primary-70 truncate flex-1 font-mono">{run.workflow}</span>
              <span className="text-[11px] text-primary-35 font-mono tabular-nums">{timeAgo(run.created_at)}</span>
            </button>
          ))}
          {!runs.length && <div className="px-[var(--space-md)] py-[var(--space-xl)] text-center text-xs text-primary-35 font-mono">No activity yet</div>}
        </div>
      </div>
    </div>
  )
}
