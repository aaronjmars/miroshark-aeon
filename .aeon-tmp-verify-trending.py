"""Throwaway sanity check for the trending sort additions."""
import sys
sys.path.insert(0, '/tmp/build-target/backend')

from app.services import gallery_filters as gf

assert 'trending' in gf.SORT_VALUES, gf.SORT_VALUES
assert gf.normalise_sort('trending') == 'trending'
assert gf.normalise_sort('TRENDING') == 'trending'
assert gf.TRENDING_FIELD == '_serves_total'


def card(sid, **kw):
    serves = kw.pop('serves_total', None)
    base = {'simulation_id': sid, 'created_at': kw.get('created_at', '2026-04-01T00:00:00')}
    base.update({k: v for k, v in kw.items() if k != 'created_at'})
    if serves is not None:
        base[gf.TRENDING_FIELD] = serves
    return base


out = gf.sort_cards([card('low', serves_total=5), card('high', serves_total=500), card('mid', serves_total=50)], sort='trending')
assert [c['simulation_id'] for c in out] == ['high', 'mid', 'low'], out

out = gf.sort_cards([
    card('stale',  serves_total=200, created_at='2026-01-01T00:00:00'),
    card('recent', serves_total=200, created_at='2026-04-30T00:00:00'),
    card('middle', serves_total=200, created_at='2026-03-15T00:00:00'),
], sort='trending')
assert [c['simulation_id'] for c in out] == ['recent', 'middle', 'stale'], out

out = gf.sort_cards([card('seen', serves_total=10), card('unseen'), card('popular', serves_total=99)], sort='trending')
assert [c['simulation_id'] for c in out] == ['popular', 'seen', 'unseen'], out

cards = [card('a', serves_total=10), card('b'), card('c', serves_total=20), card('d')]
cards[1][gf.TRENDING_FIELD] = 'not-a-number'
cards[3][gf.TRENDING_FIELD] = -50
out = gf.sort_cards(cards, sort='trending')
assert out[0]['simulation_id'] == 'c'
assert out[1]['simulation_id'] == 'a'
assert {c['simulation_id'] for c in out[2:]} == {'b', 'd'}

page, total = gf.select_filtered_cards([
    card('a', scenario='aave', final_consensus={'bullish': 70, 'neutral': 0, 'bearish': 0}, serves_total=300),
    card('b', scenario='eth',  final_consensus={'bullish': 70, 'neutral': 0, 'bearish': 0}, serves_total=999),
    card('c', scenario='aave', final_consensus={'bullish': 0,  'neutral': 0, 'bearish': 70}, serves_total=10),
], q='aave', sort='trending')
assert total == 2
assert [c['simulation_id'] for c in page] == ['a', 'c']

out = gf.sort_cards([
    card('a', serves_total=0, created_at='2026-04-01T00:00:00'),
    card('b', serves_total=0, created_at='2026-04-30T00:00:00'),
    card('c', serves_total=0, created_at='2026-04-15T00:00:00'),
], sort='trending')
assert [c['simulation_id'] for c in out] == ['b', 'c', 'a'], out

print('ALL TRENDING ASSERTIONS PASSED')
