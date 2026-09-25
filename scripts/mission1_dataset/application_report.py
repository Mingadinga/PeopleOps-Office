"""Descriptive Application/Document counts, with explicit counting units."""
import json
from collections import Counter,defaultdict

def summarize_application(data):
    eligible=data['application_eligibility'];xp=data['application_experiences'];st=[s for s in data['stage_history'] if s['stage']=='DOCUMENT_SCREEN']
    groups=defaultdict(list)
    for x in xp:groups[x['application_id']].append(x)
    combos=Counter('+'.join(sorted(json.loads(x['evidence_categories']))) or 'NONE' for x in xp)
    return {'eligibility':dict(Counter(r['overall_state'] for r in eligible)),
      'requirements':{k:dict(Counter(json.loads(r['requirement_states'])[k] for r in eligible)) for k in ['degree','language','travel_visa','military']},
      'experience_count':len(xp),'experience_combinations':dict(combos),
      'application_combinations':{combo:sum(any(('+'.join(sorted(json.loads(x['evidence_categories']))) or 'NONE')==combo for x in rows) for rows in groups.values()) for combo in combos},
      'category_applications':{cat:sum(any(cat in json.loads(x['evidence_categories']) for x in rows) for rows in groups.values()) for cat in ['PROBLEM','BUILD','VALIDATE']},
      'ownership_experiences':dict(Counter(x['ownership'] for x in xp)),
      'document_reasons':dict(Counter(s['decision_reason_code'] for s in st)),
      'note':'Application combination columns overlap for multiple experiences; category union is reporting only, never the decision rule. UNKNOWN eligibility is not verified PASS. CLOSED is insufficient submitted evidence, not Skill limitation.'}
