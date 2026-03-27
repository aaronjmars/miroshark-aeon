import sys, json

data = json.load(sys.stdin)
files = data.get('files', [])
targets = [
    'backend/scripts/round_memory.py',
    'backend/app/services/web_enrichment.py',
    'backend/wonderwall/social_agent/belief_state.py',
    'backend/scripts/run_parallel_simulation.py',
    'backend/app/services/report_agent.py',
    'backend/app/storage/neo4j_storage.py',
    'backend/app/services/oasis_profile_generator.py',
    'backend/wonderwall/simulations/polymarket/prompts.py',
    'backend/wonderwall/simulations/social_media/prompts.py',
]
limits = {
    'backend/scripts/round_memory.py': 100,
    'backend/app/services/web_enrichment.py': 80,
    'backend/wonderwall/social_agent/belief_state.py': 80,
    'backend/scripts/run_parallel_simulation.py': 120,
    'backend/app/services/report_agent.py': 120,
    'backend/app/storage/neo4j_storage.py': 80,
    'backend/app/services/oasis_profile_generator.py': 80,
    'backend/wonderwall/simulations/polymarket/prompts.py': 60,
    'backend/wonderwall/simulations/social_media/prompts.py': 80,
}
for f in files:
    if f['filename'] in targets:
        print('=== FILE:', f['filename'], '===')
        patch = f.get('patch', '')
        limit = limits.get(f['filename'], 100)
        lines = patch.split('\n')[:limit]
        print('\n'.join(lines))
        print()
