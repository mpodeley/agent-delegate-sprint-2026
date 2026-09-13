"""Create two private, revocable keys with a 24-hour access window."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import time

root = Path(__file__).resolve().parent / '.private'
root.mkdir(mode=0o700, exist_ok=True)
os.chmod(root, 0o700)
config = {'expires_at': time.time() + 24 * 3600, 'key_hashes': {}}
if (root / 'config.json').exists():
    raise SystemExit('Config already exists; refusing to replace active keys.')
for name in ('person-1', 'person-2'):
    key = 'eval-' + secrets.token_urlsafe(32)
    config['key_hashes'][name] = hashlib.sha256(key.encode()).hexdigest()
    with os.fdopen(os.open(root / f'{name}.key', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as f:
        f.write(key + '\n')
with os.fdopen(os.open(root / 'config.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'w') as f:
    json.dump(config, f, indent=2)
print('Created two private key files and config; access expires in 24 hours.')
