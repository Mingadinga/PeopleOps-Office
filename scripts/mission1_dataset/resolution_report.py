"""Descriptive counts separating evidence qualification and resolved eligibility."""
import json
from collections import Counter,defaultdict

def summarize_resolution(data):
    initial={r['application_id']:r for r in data['application_eligibility']};events=defaultdict(list)
    for e in data['eligibility_verifications']:events[e['application_id']].append(e)
    def final_status(aid):
        statuses=json.loads(initial[aid]['requirement_states'])
        for e in events[aid]:statuses[e['requirement']]=e['resulting_status']
        return 'FAIL' if 'FAIL' in statuses.values() else 'UNKNOWN' if 'UNKNOWN' in statuses.values() else 'PASS'
    doc=[s for s in data['stage_history'] if s['stage']=='DOCUMENT_SCREEN'];outcomes=Counter()
    for s in doc:
        if s['result']!='CONDITIONAL_ADVANCE':continue
        rows=events[s['application_id']];results={e['verification_result'] for e in rows}
        outcome='VERIFIED_FAIL' if 'VERIFIED_FAIL' in results else 'PENDING' if not rows or 'PENDING' in results else 'ELIGIBILITY_NOT_VERIFIED' if 'ELIGIBILITY_NOT_VERIFIED' in results else 'VERIFIED_PASS'
        outcomes[outcome]+=1
    candidate_app={a['candidate_id']:a['application_id'] for a in data['applications']}
    return {'initial':dict(Counter(r['overall_state'] for r in initial.values())),
      'document_states':dict(Counter(s['result'] for s in doc)),
      'document_evidence_qualified':sum(s['result'] in ('ADVANCED','CONDITIONAL_ADVANCE') for s in doc),
      'verification_candidates':dict(outcomes),'verification_requirements':dict(Counter(e['verification_result'] for e in data['eligibility_verifications'])),
      'pre_entry':sum(s['stage']=='PRE_ASSESSMENT' for s in data['stage_history']),
      'offer_unresolved':sum(final_status(o['application_id'])!='PASS' for o in data['offers']),
      'join_unresolved':sum(final_status(candidate_app[p['source_candidate_id']])!='PASS' for p in data['onboarding_profiles']),
      'note':'Document conditional decision remains history; original UNKNOWN is never rewritten. NOT_VERIFIED is procedure closure, not eligibility FAIL or Skill limitation.'}
