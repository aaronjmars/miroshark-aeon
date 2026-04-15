'use client'

import { useState } from 'react'
import { inputCls } from '../lib/utils'

interface AuthModalProps {
  loading: boolean
  onClose: () => void
  onAuth: (key: string) => void
}

export function AuthModal({ loading, onClose, onAuth }: AuthModalProps) {
  const [authKey, setAuthKey] = useState('')

  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/30 backdrop-blur-sm">
      <div className="bg-white border-2 border-[rgba(10,10,10,0.08)] w-full max-w-sm mx-4 p-[var(--space-lg)] shadow-2xl">
        <div className="flex items-center justify-between mb-[var(--space-sm)]">
          <h2 className="font-display text-xl">Authenticate</h2>
          <button onClick={onClose} className="text-primary-35 hover:text-primary-100 text-lg">&times;</button>
        </div>
        <p className="text-xs text-primary-50 font-mono mb-[var(--space-md)]">Paste your API key to enable deployments.</p>
        <input type="password" value={authKey} onChange={(e) => setAuthKey(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && authKey.trim() && onAuth(authKey.trim())} placeholder="sk-ant-..." autoFocus className={`${inputCls} mb-[var(--space-md)]`} />
        <button onClick={() => onAuth(authKey.trim())} disabled={!authKey.trim() || loading} className="w-full bg-eva-black text-white text-sm py-3 font-mono uppercase tracking-[2px] hover:opacity-90 transition-opacity disabled:opacity-50">{loading ? '...' : 'Save'}</button>
      </div>
    </div>
  )
}
