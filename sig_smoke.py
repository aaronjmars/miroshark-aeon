import sys, os
sys.path.insert(0, '/tmp/build-target/backend')
from app.services.webhook_service import compute_signature, verify_signature, SIGNATURE_HEADER, SIGNATURE_PREFIX

os.environ.pop('WEBHOOK_SECRET', None)
assert compute_signature(b'body', '') is None
assert compute_signature(b'body') is None

sig = compute_signature(b'{"a":1}', 'shh')
print('sig:', sig)
assert sig.startswith('sha256=')
hex_part = sig[len('sha256='):]
assert len(hex_part) == 64
assert verify_signature(b'{"a":1}', sig, 'shh') is True
assert verify_signature(b'{"a":2}', sig, 'shh') is False
assert verify_signature(b'{"a":1}', sig, 'wrong') is False
flipped = sig[:-1] + ('0' if sig[-1] != '0' else '1')
assert verify_signature(b'{"a":1}', flipped, 'shh') is False
assert verify_signature(b'{"a":1}', '', 'shh') is False
assert verify_signature(b'{"a":1}', None, 'shh') is False

os.environ['WEBHOOK_SECRET'] = '  '
assert compute_signature(b'x') is None
os.environ['WEBHOOK_SECRET'] = 'real-secret'
got = compute_signature(b'x')
assert got is not None
assert verify_signature(b'x', got, 'real-secret') is True

print('SIGNATURE_HEADER =', SIGNATURE_HEADER)
print('SIGNATURE_PREFIX =', SIGNATURE_PREFIX)
print('All assertions passed.')
