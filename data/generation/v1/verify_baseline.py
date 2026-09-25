"""Read-only v1 freeze verification: python3 -B data/generation/v1/verify_baseline.py."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts.mission1_dataset.common import read_data, load_rules, file_hashes  # noqa: E402
from scripts.mission1_dataset.validate import validate, validate_manifest  # noqa: E402
from scripts.mission1_dataset.report import summarize  # noqa: E402


def verify(root=ROOT):
    errors = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    def read(relative):
        return json.loads((root / relative).read_text(encoding='utf-8'))

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    meta = root / 'data/generation/v1'
    source = root / 'data/generated/v0.4'
    baseline = root / 'data/synthetic/v1'
    manifest = read('data/generation/v1/dataset_manifest.json')
    original = read('data/generation/v0.4/dataset_manifest.json')
    rules_path = root / 'data/generation/v0.4/generation_rules.json'
    rules = load_rules(rules_path)
    data = read_data(baseline)
    validation = validate(data, rules)
    errors.extend('invariant: ' + str(e) for e in validation['errors'])
    # Candidate manifest validates source provenance against the promoted bytes.
    errors.extend('source manifest: ' + str(e) for e in
                  validate_manifest(original, data, rules, baseline, rules_path))
    expected = original['file_sha256']
    check(file_hashes(source) == file_hashes(baseline) == expected == manifest['file_sha256'], 'Canonical hashes differ')
    check({p.name for p in baseline.iterdir()} == set(expected), 'Unexpected/missing baseline files')
    check(manifest['dataset_version'] == 'v1' and manifest['source_candidate_version'] == 'v0.4', 'Version mismatch')
    check(manifest['dataset_path'] == 'data/synthetic/v1', 'Baseline path mismatch')
    check(manifest['seed'] == manifest['source_seed'] == rules['seed'] == 20260924, 'Seed mismatch')
    check(manifest['baseline_status'] == 'FROZEN' and manifest['frozen'] is True, 'Not frozen')
    check(manifest['review_status'] == manifest['human_review_status'] == 'APPROVED', 'Missing approval')
    check(bool(manifest['approval_basis']), 'Missing Human Review authority')
    frozen = datetime.fromisoformat(manifest['frozen_at'])
    check(frozen.utcoffset() is not None and manifest['approved_at'] == manifest['frozen_at'], 'Invalid approval timestamp')
    check(manifest['synthetic_data'] is True and 'not Kia internal' in manifest['disclaimer'], 'Missing synthetic disclaimer')
    check(manifest['source_manifest_ref'] == 'data/generation/v0.4/dataset_manifest.json', 'Wrong source reference')
    check(manifest['source_manifest_sha256'] == digest(root / manifest['source_manifest_ref']), 'Source manifest hash mismatch')
    check(manifest['generation_rules_ref'] == 'data/generation/v0.4/generation_rules.json', 'Wrong rules reference')
    for field in ('generation_version', 'generation_rules_version', 'schema_version', 'generated_at',
                  'observation_start', 'observation_end', 'timezone', 'case_id', 'job_id', 'record_counts',
                  'generation_rules_sha256', 'generator_source_sha256', 'implementation_parameters',
                  'random_stream_version', 'capacity_parameters', 'source_matrix', 'response_window_days'):
        check(manifest[field] == original[field], 'Provenance mismatch: ' + field)
    check(manifest['validation_status'] == 'PASS' and manifest['validation_errors'] == [], 'Wrong validation status')
    for name in ('human_review_snapshot.json', 'synthetic_assumptions.json'):
        check(manifest['metadata_sha256'].get(name) == digest(meta / name), 'Metadata hash mismatch: ' + name)
    assumptions = read('data/generation/v1/synthetic_assumptions.json')
    check(assumptions['dataset_version'] == 'v1' and assumptions['synthetic_data'] is True, 'Wrong assumption scope')
    expected_ids = {'evaluator_pool', 'additional_capacity', 'calibration', 'evidence_distribution',
                    'evaluator_interpretation', 'targeted_followup', 'offer_response', 'mentor_ready',
                    'calendar_scope', 'public_requirements'}
    check({a['id'] for a in assumptions['assumptions']} == expected_ids, 'Missing synthetic assumption')
    snapshot = read('data/generation/v1/human_review_snapshot.json')
    check(snapshot['dataset_version'] == 'v1' and snapshot['source_candidate_version'] == 'v0.4'
          and snapshot['approved_at'] == manifest['approved_at'] and snapshot['review_status'] == 'APPROVED', 'Wrong review snapshot')
    actual = summarize(data, rules, validation)
    for key, value in snapshot['metrics'].items():
        check(value == actual[key], 'Approved snapshot differs from actual: ' + key)
    registry = read('data/generation/baseline_registry.json')
    active = [entry for entry in registry['baselines'] if entry['status'] == 'ACTIVE']
    check(registry['active_baseline'] == 'v1' and len(active) == 1 and active[0]['dataset_version'] == 'v1', 'Wrong active baseline')
    entry = next(e for e in registry['baselines'] if e['dataset_version'] == 'v1')
    check(entry['source_candidate_version'] == 'v0.4' and entry['superseded_by'] is None
          and entry['approved_at'] == manifest['approved_at'] and bool(entry['change_reason']), 'Wrong registry provenance')
    check(entry['manifest_ref'] == 'data/generation/v1/dataset_manifest.json'
          and entry['manifest_sha256'] == digest(meta / 'dataset_manifest.json'), 'Registry manifest hash mismatch')
    return {'dataset_version': 'v1', 'status': 'PASS' if not errors else 'ERROR', 'errors': errors,
            'canonical_file_count': len(expected), 'content_identity': not errors,
            'independent_validation_status': validation['status'], 'independent_checks': validation['checks'],
            'source_validation_warnings': validation['warnings'],
            'human_review_status': 'APPROVED', 'synthetic_assumptions_ref': 'data/generation/v1/synthetic_assumptions.json'}


if __name__ == '__main__':
    result = verify()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
