export const MODELS = [
  { id: 'claude-opus-4-6', label: 'Opus 4.6' },
  { id: 'claude-sonnet-4-6', label: 'Sonnet 4.6' },
  { id: 'claude-haiku-4-5-20251001', label: 'Haiku 4.5' },
]

export const DAYS = [
  { label: 'All', value: -1 }, { label: 'Mon', value: 1 }, { label: 'Tue', value: 2 },
  { label: 'Wed', value: 3 }, { label: 'Thu', value: 4 }, { label: 'Fri', value: 5 },
  { label: 'Sat', value: 6 }, { label: 'Sun', value: 0 },
]

export const DEPARTMENTS: Record<string, { label: string; color: string }> = {
  meta:     { label: 'Operations',     color: '#6B7280' },
  crypto:   { label: 'Treasury',       color: '#FF6B1A' },
  dev:      { label: 'Engineering',    color: '#3B82F6' },
  news:     { label: 'Intelligence',   color: '#06B6D4' },
  social:   { label: 'Communications', color: '#EC4899' },
  research: { label: 'R&D',            color: '#8B5CF6' },
  content:  { label: 'Publishing',     color: '#43C165' },
  creative: { label: 'Creative',       color: '#F59E0B' },
}
