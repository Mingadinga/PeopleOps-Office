"""Read-only active/historical baseline verification; no generation or writes."""
import hashlib
import json
import sys
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.mission1_dataset.common import read_data, load_rules, file_hashes  # noqa: E402
from scripts.mission1_dataset.validate import validate, validate_manifest  # noqa: E402
from scripts.mission1_dataset.report import summarize  # noqa: E402


def verify(version="v2", root=ROOT):
    errors = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    def read(relative):
        return json.loads((root / relative).read_text(encoding='utf-8'))

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    if version not in ('v1', 'v2'):
        raise ValueError('Unknown baseline version')
    candidate = {'v1': 'v0.4', 'v2': 'v0.6'}[version]
    meta = root / f'data/generation/{version}'
    source = root / f'data/generated/{candidate}'
    baseline = root / f'data/synthetic/{version}'
    manifest = read(f'data/generation/{version}/dataset_manifest.json')
    original = read(f'data/generation/{candidate}/dataset_manifest.json')
    rules_path = root / f'data/generation/{candidate}/generation_rules.json'
    rules = load_rules(rules_path)
    data = read_data(baseline)
    validation = validate(data, rules)
    errors.extend('invariant: ' + str(e) for e in validation['errors'])
    # Candidate manifest validates source provenance against the promoted bytes.
    manifest_errors = validate_manifest(original, data, rules, baseline, rules_path)
    if version == 'v1':
        # Historical code must match its recorded commit, not today's generator.
        history_ok = True
        for name, expected_hash in original['generator_source_sha256'].items():
            try:
                historical = subprocess.check_output(
                    ['git', 'show', manifest['source_git_commit'] + ':scripts/mission1_dataset/' + name],
                    cwd=ROOT, stderr=subprocess.DEVNULL)
                history_ok &= hashlib.sha256(historical).hexdigest() == expected_hash
            except subprocess.CalledProcessError:
                history_ok = False
        check(history_ok, 'Historical generator commit hash mismatch')
        if history_ok:
            manifest_errors = [e for e in manifest_errors if e['message'] !=
                               'Generator source differs; regenerate/review candidate after implementation fixes']
    errors.extend('source manifest: ' + str(e) for e in manifest_errors)
    expected = original['file_sha256']
    check(file_hashes(source) == file_hashes(baseline) == expected == manifest['file_sha256'], 'Canonical hashes differ')
    check({p.name for p in baseline.iterdir()} == set(expected), 'Unexpected/missing baseline files')
    check(manifest['dataset_version'] == version and manifest['source_candidate_version'] == candidate, 'Version mismatch')
    check(manifest['dataset_path'] == f'data/synthetic/{version}', 'Baseline path mismatch')
    check(manifest['seed'] == manifest['source_seed'] == rules['seed'] == 20260924, 'Seed mismatch')
    check(manifest['baseline_status'] == 'FROZEN' and manifest['frozen'] is True, 'Not frozen')
    check(manifest['review_status'] == manifest['human_review_status'] == 'APPROVED', 'Missing approval')
    check(bool(manifest['approval_basis']), 'Missing Human Review authority')
    frozen = datetime.fromisoformat(manifest['frozen_at'])
    check(frozen.utcoffset() is not None and manifest['approved_at'] == manifest['frozen_at'], 'Invalid approval timestamp')
    check(manifest['synthetic_data'] is True and 'not Kia internal' in manifest['disclaimer'], 'Missing synthetic disclaimer')
    check(manifest['source_manifest_ref'] == f'data/generation/{candidate}/dataset_manifest.json', 'Wrong source reference')
    check(manifest['source_manifest_sha256'] == digest(root / manifest['source_manifest_ref']), 'Source manifest hash mismatch')
    check(manifest['generation_rules_ref'] == f'data/generation/{candidate}/generation_rules.json', 'Wrong rules reference')
    for field in ('generation_version', 'generation_rules_version', 'schema_version', 'generated_at',
                  'observation_start', 'observation_end', 'timezone', 'case_id', 'job_id', 'record_counts',
                  'generation_rules_sha256', 'generator_source_sha256', 'implementation_parameters',
                  'random_stream_version', 'capacity_parameters', 'source_matrix', 'response_window_days'):
        check(manifest[field] == original[field], 'Provenance mismatch: ' + field)
    check(manifest['validation_status'] == 'PASS' and manifest['validation_errors'] == [], 'Wrong validation status')
    for name in ('human_review_snapshot.json', 'synthetic_assumptions.json'):
        check(manifest['metadata_sha256'].get(name) == digest(meta / name), 'Metadata hash mismatch: ' + name)
    assumptions = read(f'data/generation/{version}/synthetic_assumptions.json')
    check(assumptions['dataset_version'] == version and assumptions['synthetic_data'] is True, 'Wrong assumption scope')
    expected_ids = {'evaluator_pool', 'additional_capacity', 'calibration', 'evidence_distribution',
                    'evaluator_interpretation', 'targeted_followup', 'offer_response', 'mentor_ready',
                    'calendar_scope', 'public_requirements'}
    if version == 'v2':
        expected_ids |= {'eligibility_population', 'verification_timing', 'verification_outcomes',
                         'application_experiences', 'ownership', 'eligibility_dates'}
    check({a['id'] for a in assumptions['assumptions']} == expected_ids, 'Missing synthetic assumption')
    snapshot = read(f'data/generation/{version}/human_review_snapshot.json')
    check(snapshot['dataset_version'] == version and snapshot['source_candidate_version'] == candidate
          and snapshot['approved_at'] == manifest['approved_at'] and snapshot['review_status'] == 'APPROVED', 'Wrong review snapshot')
    actual = summarize(data, rules, validation)
    def contained(expected, current):
        # Later reports may add fields; historical approval values cannot change.
        if isinstance(expected, dict):
            return isinstance(current, dict) and all(k in current and contained(v, current[k]) for k, v in expected.items())
        if isinstance(expected, list):
            return isinstance(current, list) and len(expected) == len(current) and all(contained(a, b) for a, b in zip(expected, current))
        return expected == current

    for key, value in snapshot['metrics'].items():
        check(contained(value, actual.get(key)), 'Approved snapshot differs from actual: ' + key)
    if version == 'v2':
        check(snapshot.get('candidate_review_status') == 'APPROVED FOR BASELINE PROMOTION', 'Candidate approval missing')
        check(len(snapshot.get('approved_decisions', [])) == 3, 'Missing explicit Human Review decisions')
        resolution = actual['eligibility_resolution']
        check(resolution['offer_unresolved'] == resolution['join_unresolved'] == 0, 'Unresolved eligibility at Offer/Join')
        # Rules and generator provenance are current for this promotion; legacy manifests remain historical.
        check(original['generator_source_sha256'] == {
            p.name: digest(p) for p in (root / 'scripts/mission1_dataset').glob('*.py')
        }, 'Generator source provenance mismatch')
    registry = read('data/generation/baseline_registry.json')
    active = [entry for entry in registry['baselines'] if entry['status'] == 'ACTIVE']
    check(len(active) == 1 and active[0]['dataset_version'] == registry['active_baseline'] == 'v2', 'Wrong active baseline')
    check(len({e['dataset_version'] for e in registry['baselines']}) == len(registry['baselines']), 'Duplicate registry version')
    entry = next(e for e in registry['baselines'] if e['dataset_version'] == version)
    check(entry['source_candidate_version'] == candidate and entry['superseded_by'] == (None if version == 'v2' else 'v2')
          and entry['status'] == ('ACTIVE' if version == 'v2' else 'SUPERSEDED')
          and entry['approved_at'] == manifest['approved_at'] and bool(entry['change_reason']), 'Wrong registry provenance')
    check(entry['manifest_ref'] == f'data/generation/{version}/dataset_manifest.json'
          and entry['manifest_sha256'] == digest(meta / 'dataset_manifest.json'), 'Registry manifest hash mismatch')
    return {'dataset_version': version, 'status': 'PASS' if not errors else 'ERROR', 'errors': errors,
            'canonical_file_count': len(expected), 'content_identity': not errors,
            'independent_validation_status': validation['status'], 'independent_checks': validation['checks'],
            'source_validation_warnings': validation['warnings'],
            'human_review_status': 'APPROVED', 'synthetic_assumptions_ref': f'data/generation/{version}/synthetic_assumptions.json'}


if __name__ == '__main__':
    result = verify(sys.argv[1] if len(sys.argv) > 1 else 'v2')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
