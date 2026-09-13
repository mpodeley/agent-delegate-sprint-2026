"""Freeze only experiment inputs; never copy provider configuration or credentials."""
import hashlib
import json
import platform
from importlib.metadata import version, PackageNotFoundError
import shutil
import subprocess
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def freeze_inputs(root, pair, out):
    root, pair, out = map(Path, (root, pair, out))
    snapshot = out / 'inputs'
    snapshot.mkdir()
    # Explicit source allowlist includes new uncommitted modules but excludes private configs.
    sources = set(root.glob('*.py')) | set(root.glob('*.txt'))
    sources |= {root / name for name in ('Dockerfile', 'pyproject.toml', 'uv.lock', 'experiment.json', 'rates.json')}
    sources |= {p for p in (root / 'board').rglob('*') if p.is_file()}
    for path in sorted(sources):
        target = snapshot / 'source' / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    # Evaluator-side flags are task inputs, not credentials. Never exposed to the worker.
    shutil.copytree(pair, snapshot / 'fixture')
    hashes = {str(p.relative_to(snapshot)): digest(p) for p in sorted(snapshot.rglob('*')) if p.is_file()}
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
    provenance = {'git_commit': git('rev-parse', 'HEAD'), 'git_branch': git('branch', '--show-current'),
                  'git_dirty': bool(git('status', '--porcelain', '--', str(root))),
                  'files': hashes, 'input_sha256': hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()}
    images = set()
    for compose in (snapshot / 'fixture').glob('*/compose.json'):
        images.update(s['image'] for s in json.loads(compose.read_text())['services'].values())
    provenance['docker_images'] = {}
    for name in sorted(images):
        raw = subprocess.check_output(['docker', 'image', 'inspect', name], text=True)
        item = json.loads(raw)[0]
        provenance['docker_images'][name] = {'id': item['Id'], 'repo_digests': item.get('RepoDigests', [])}
    packages = {}
    for name in ('inspect-ai', 'control-tower'):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = 'unavailable'
    provenance['runtime'] = {'python': platform.python_version(), 'packages': packages,
                             'docker_images': provenance['docker_images']}
    provenance['runtime_sha256'] = hashlib.sha256(json.dumps(provenance['runtime'],sort_keys=True).encode()).hexdigest()
    (out / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    return provenance


def runtime_artifacts(out):
    """Record CT-generated runtime files separately from inputs frozen before execution."""
    out = Path(out)
    provenance_path = out / 'provenance.json'
    if not provenance_path.exists():
        return {}
    known = json.loads(provenance_path.read_text())['files']
    return {str(p.relative_to(out/'inputs')): digest(p)
            for p in sorted((out/'inputs').rglob('*'))
            if p.is_file() and str(p.relative_to(out/'inputs')) not in known}


def verify_inputs(out):
    out = Path(out)
    p = json.loads((out / 'provenance.json').read_text())
    errors = []
    for name, expected in p['files'].items():
        path = out / 'inputs' / name
        if not path.is_file() or digest(path) != expected:
            errors.append(name)
    actual = hashlib.sha256(json.dumps(p['files'], sort_keys=True).encode()).hexdigest()
    if actual != p['input_sha256']:
        errors.append('input_sha256')
    manifest = json.loads((out / 'manifest.json').read_text())
    if manifest.get('input_sha256') != actual:
        errors.append('manifest.input_sha256')
    generated = runtime_artifacts(out)
    if generated != manifest.get('runtime_artifacts', {}):
        errors.append('runtime_artifacts')
    runtime_hash = hashlib.sha256(json.dumps(p['runtime'],sort_keys=True).encode()).hexdigest()
    if runtime_hash != p['runtime_sha256'] or manifest.get('runtime_sha256') != runtime_hash:
        errors.append('runtime_sha256')
    return errors
