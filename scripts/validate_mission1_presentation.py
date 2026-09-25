"""Read-only validation of the v1 presentation mapping; no hiring decisions."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = 'presentation/mission1_representative_cases.json'
EXPECTED = [('CASE_A', 'C0003', 'APP0003', 'M1_SKILL_02'),
            ('CASE_B', 'C0005', 'APP0005', 'M1_SKILL_04'),
            ('CASE_C', 'C0228', 'APP0228', 'M1_SKILL_04')]


def validate(mapping, root=ROOT):
    errors = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    base = root / 'data/synthetic/v1'
    manifest_path = root / 'data/generation/v1/dataset_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    registry = json.loads((root / 'data/generation/baseline_registry.json').read_text())
    check(mapping.get('mapping_version') == '1.0.0' and mapping.get('dataset_version') == 'v1', 'version binding')
    check(mapping.get('baseline_manifest_ref') == 'data/generation/v1/dataset_manifest.json', 'manifest reference')
    check(mapping.get('baseline_manifest_sha256') == hashlib.sha256(manifest_path.read_bytes()).hexdigest(), 'manifest hash')
    check(manifest['dataset_version'] == 'v1' and manifest['review_status'] == 'APPROVED' and manifest['frozen'], 'approved baseline')
    check(any(b['dataset_version'] == 'v1' for b in registry['baselines']), 'registered baseline')
    check({p.name for p in base.iterdir()} == set(manifest['file_sha256']), 'canonical file list')
    for name, digest in manifest['file_sha256'].items():
        check(hashlib.sha256((base / name).read_bytes()).hexdigest() == digest, 'canonical hash: ' + name)
    data = {p.stem: list(csv.DictReader(p.open(encoding='utf-8'))) for p in base.glob('*.csv')}
    idx = {table: {row[next(iter(row))]: row for row in rows} for table, rows in data.items()}
    doc = (root / 'docs/06_mission1_experience_specification.md').read_text()
    relations = {}
    for row in data['skill_decision_observations']:
        relations.setdefault(row['decision_id'], []).append(row['observation_id'])

    def owner(table, row):
        if table in ('assessment_activities', 'assessment_evidence', 'assessment_observations',
                     'evidence_decisions', 'stage_history', 'final_decisions', 'offers'):
            return row['application_id']
        if table == 'calibration_reviews':
            return idx['stage_history'][row['stage_event_id']]['application_id']
        if table == 'targeted_followups':
            return idx['assessment_evidence'][row['evidence_id']]['application_id']
        if table == 'activity_sessions':
            return idx['assessment_activities'][row['activity_id']]['application_id']
        if table == 'offer_events':
            return idx['offers'][row['offer_id']]['application_id']
        return None

    cases = mapping.get('cases', [])
    check([(c.get('case_id'), c.get('candidate_id'), c.get('application_id'), c.get('primary_skill_id')) for c in cases] == EXPECTED, 'human-selected identities')
    for case in cases:
        aid = case['application_id']; sid = case['primary_skill_id']
        app = idx['applications'].get(aid)
        check(app is not None and app['candidate_id'] == case['candidate_id'], 'candidate/application identity')
        check(bool(case.get('presentation_question')) and bool(case.get('core_message')) and bool(case.get('caveats')), 'presentation copy')
        check(2 <= len(case.get('evidence_cards', [])) <= 4, 'evidence card count')
        refs = {}
        groups = [case.get('refs', {}), case.get('secondary_lifecycle_refs', {})]
        groups += [step.get('refs', {}) for step in case.get('steps', [])]
        for group in groups:
            for table, keys in group.items():
                check(table in idx, 'unknown reference table: ' + table)
                for key in keys:
                    refs.setdefault(table, set()).add(key)
                    row = idx.get(table, {}).get(key)
                    check(row is not None, 'missing reference: ' + key)
                    if row:
                        check(owner(table, row) == aid, 'foreign candidate reference: ' + key)
        check(case.get('scene_refs') == list(dict.fromkeys(s['scene_ref'] for s in case['steps'])), 'scene order')
        for step in case['steps']:
            heading = '### ' + step['scene_ref'] + '.'
            check(heading in doc, 'unknown scene')
            if heading in doc:
                section = doc.split(heading, 1)[1].split('\n### ', 1)[0]
                space = re.search(r'\*\*Stage / Space:\*\* .* / (.+)', section).group(1)
                roles = re.search(r'\*\*Participants:\*\* (.+)', section).group(1).split(', ')
                check(step['space_label'] == space and step['human_roles'] == roles, 'scene space/role contract')
        for card in case.get('evidence_cards', []):
            eid = card['evidence_id']; evidence = idx['assessment_evidence'].get(eid)
            check(evidence is not None and evidence['application_id'] == aid, 'card evidence owner')
            check(eid in refs.get('assessment_evidence', set()), 'card lacks step reference')
            observations = [o for o in data['assessment_observations'] if o['evidence_id'] == eid]
            check(bool(observations) and {o['observation_id'] for o in observations} <= refs.get('assessment_observations', set()), 'card observation lineage')
            linked = {link['confirmed_skill_id'] for link in data['evidence_skill_links'] if link['evidence_id'] == eid and link['confirmation_status'] in ('CONFIRMED', 'MODIFIED')}
            check((sid in linked) == (card['purpose'] == 'PRIMARY_SKILL'), 'card skill boundary')
        for did in refs.get('evidence_decisions', set()):
            decision = idx['evidence_decisions'].get(did)
            if not decision:
                continue
            observations = [idx['assessment_observations'].get(o) for o in relations.get(did, [])]
            check(bool(observations) and all(o and o['application_id'] == aid and o['skill_id'] == decision['skill_id'] for o in observations), 'decision observation lineage')
        first = idx['stage_history'].get(aid + '_FIRST_INTERVIEW')
        check(first is not None, 'FIRST stage')
        if case['case_id'] == 'CASE_A':
            coverage = json.loads(first['rationale'])['coverage'][sid]
            check(first['result'] == 'IN_PROGRESS' and first['decision_reason_code'] == 'EVIDENCE_PENDING' and not coverage['decisionable'], 'A evidence pending')
            check(coverage['skill_decision_ref'] in refs.get('evidence_decisions', set()), 'A coverage decision reference')
            check(not refs.get('final_decisions') and not any(f['application_id'] == aid for f in data['final_decisions']), 'A must not invent final review')
        else:
            initial = idx['final_decisions'][f'FD_{aid}_INITIAL']; rer = idx['final_decisions'][f'FD_{aid}_RE_REVIEW']
            check({initial['final_decision_id'], rer['final_decision_id']} <= refs.get('final_decisions', set()), 'HOLD/final reference')
            check(initial['decision'] == 'HOLD' and rer['decision'] != 'HOLD', 'HOLD lifecycle')
            check(rer['decision'] == ('DO_NOT_PROCEED' if case['case_id'] == 'CASE_B' else 'PROCEED_TO_OFFER'), 'approved final outcome')
            plans = [p for p in json.loads(initial['resolution_plan']) if p['skill_id'] == sid]
            check(len(plans) == 1, 'resolution plan skill')
            check(any(s.get('resolution_plan_ref') == {'final_decision_id': initial['final_decision_id'], 'skill_id': sid} for s in case['steps']), 'resolution plan reference')
            for step in case['steps']:
                if 'resolution_plan_ref' in step:
                    check(step['resolution_plan_ref'] == {'final_decision_id': initial['final_decision_id'], 'skill_id': sid}, 'foreign resolution plan reference')
            for decision in (initial, rer):
                decisions = [idx['evidence_decisions'][key] for key in json.loads(decision['rationale'])['decision_refs']]
                primary = next(d for d in decisions if d['skill_id'] == sid)
                check(primary['decision_id'] in refs.get('evidence_decisions', set()), 'final skill snapshot reference')
            follow = [f for f in data['targeted_followups'] if f['hold_decision_id'] == initial['final_decision_id'] and f['skill_id'] == sid]
            check(len(follow) == 1 and follow[0]['evidence_id'] in refs.get('targeted_followups', set()), 'targeted follow-up reference')
            if follow:
                item = follow[0]; expected = 'ARTIFACT_UNAVAILABLE' if case['case_id'] == 'CASE_B' else 'OWNERSHIP_TRACE_SUPPLIED'
                check(item['response_kind'] == expected and item['question'] == plans[0]['question'] and item['hold_reason'] == plans[0]['reason'], 'targeted question/response')
                new_obs = {o['observation_id'] for o in data['assessment_observations'] if o['evidence_id'] == item['evidence_id']}
                check(any(new_obs & set(relations[did]) for did in json.loads(rer['rationale'])['decision_refs']), 'follow-up to re-review lineage')
                check(initial['follow_up_activity_id'] in refs.get('assessment_activities', set()), 'follow-up activity reference')
    contract = mapping.get('presentation_contract', {})
    check(contract.get('card_title_field') == 'presentation_question' and contract.get('identity_visibility') == 'DETAILS_ONLY', 'question-first cards')
    check(contract.get('human_dialogue_typing') is False and contract.get('live_ai_evaluation') is False and contract.get('decision_reveal') == 'STORED_V1_TRACE_ONLY', 'stored trace reveal contract')
    return {'status': 'ERROR' if errors else 'PASS', 'dataset_version': 'v1', 'cases_checked': len(cases), 'errors': errors}


if __name__ == '__main__':
    result = validate(json.loads((ROOT / MAPPING).read_text(encoding='utf-8')))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'PASS')
