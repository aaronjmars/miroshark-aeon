export interface Skill { name: string; description: string; tags: string[]; enabled: boolean; schedule: string; var: string; model: string }
export interface Run { id: number; workflow: string; status: string; conclusion: string | null; created_at: string; url: string }
export interface Secret { name: string; group: string; description: string; isSet: boolean; either?: string }
export interface SkillOutput { filename: string; skill: string; timestamp: string; spec: { root: string; state?: Record<string, unknown>; elements: Record<string, SpecElement> } }
export interface SpecElement { type: string; props?: Record<string, unknown>; children?: string[] }
