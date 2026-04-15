export function ErrorScreen({ error }: { error: string }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-grid">
      <div className="card-hst p-[var(--space-lg)] corner-markers max-w-sm">
        <div className="corner-marker corner-marker-sm top-left" />
        <div className="corner-marker corner-marker-sm top-right" />
        <div className="corner-marker corner-marker-sm bottom-left" />
        <div className="corner-marker corner-marker-sm bottom-right" />
        <div className="text-center">
          <p className="font-display text-xl text-eva-red mb-2">Connection Error</p>
          <div className="warning-stripes my-3" />
          <p className="text-xs text-primary-50 font-mono">{error}</p>
        </div>
      </div>
    </div>
  )
}
