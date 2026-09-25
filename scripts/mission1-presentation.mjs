// Read-only, build-time projection. Never generates or writes recruiting records.
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
export const root = fileURLToPath(new URL('../', import.meta.url));
const read = file => readFileSync(path.join(root, file), 'utf8');
const json = file => JSON.parse(read(file));
const hash = text => createHash('sha256').update(text).digest('hex');
export function csv(text) {
  const rows = []; let row = [], field = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') { if (quoted && text[i + 1] === '"') { field += '"'; i++; } else quoted = !quoted; }
    else if (c === ',' && !quoted) { row.push(field); field = ''; }
    else if (c === '\n' && !quoted) { row.push(field.replace(/\r$/, '')); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  const headers = rows.shift();
  return rows.map(values => Object.fromEntries(headers.map((key, i) => [key, values[i] ?? ''])));
}
const decode = value => { try { return JSON.parse(value); } catch { return value; } };
const uniq = (rows, key) => new Set(rows.map(r => r[key])).size;
const sum = rows => rows.reduce((n, r) => n + Number(r.person_hours), 0);
export function project() {
  const mapping = json('presentation/mission1_representative_cases.json');
  const manifest = json(mapping.baseline_manifest_ref);
  if (mapping.dataset_version !== 'v1' || manifest.review_status !== 'APPROVED' || hash(read(mapping.baseline_manifest_ref)) !== mapping.baseline_manifest_sha256) throw Error('Unapproved or mismatched baseline');
  const source = manifest.dataset_path;
  const tables = {};
  for (const [file, digest] of Object.entries(manifest.file_sha256)) {
    const text = read(`${source}/${file}`);
    if (hash(text) !== digest) throw Error(`Canonical hash mismatch: ${file}`);
    tables[file.replace(/\.(csv|json)$/, '')] = file.endsWith('.csv') ? csv(text).map(row => Object.fromEntries(Object.entries(row).map(([k, v]) => [k, decode(v)]))) : JSON.parse(text);
  }
  const t = tables, stages = t.stage_history, events = t.workforce_events;
  const entered = stage => stages.filter(r => r.stage === stage && r.entered_at);
  const advanced = stage => stages.filter(r => r.stage === stage && r.result === 'ADVANCED');
  const joined = events.filter(r => r.event_type === 'JOINED');
  const ready = events.filter(r => r.event_type === 'READY_CONFIRMED');
  const counts = [uniq(t.applications.filter(r => r.started_at), 'candidate_id'), uniq(t.applications.filter(r => r.submitted_at), 'candidate_id'), uniq(advanced('DOCUMENT_SCREEN'), 'candidate_id'), uniq(advanced('PRE_ASSESSMENT'), 'candidate_id'), uniq(entered('FIRST_INTERVIEW'), 'candidate_id'), uniq(entered('SECOND_INTERVIEW'), 'candidate_id'), uniq(t.offers, 'candidate_id'), uniq(joined, 'employee_id')];
  const cap = t.interview_capacity_events;
  const initial = cap.find(r => r.event_type === 'INITIAL_PLAN');
  const demand = cap.find(r => r.event_type === 'GAP_IDENTIFIED');
  const added = cap.filter(r => r.event_type === 'CAPACITY_ADDED');
  const plan = t.funnel_plan.find(r => r.stage === 'FIRST_INTERVIEW');
  const ids = { assessment_evidence: 'evidence_id', assessment_observations: 'observation_id', evidence_decisions: 'decision_id', stage_history: 'stage_event_id', final_decisions: 'final_decision_id', calibration_reviews: 'review_id', assessment_activities: 'activity_id', targeted_followups: 'evidence_id' };
  const get = (table, id) => {
    const found = t[table].find(r => r[ids[table]] === id);
    if (!found) throw Error(`Missing presentation reference ${table}/${id}`);
    return found;
  };
  const skills = t.talent_profile;
  const cases = mapping.cases.map(c => ({
    id: c.case_id, candidateId: c.candidate_id, applicationId: c.application_id,
    question: c.presentation_question, message: c.core_message, skill: skills.find(s => s.skill_id === c.primary_skill_id), caveats: c.caveats,
    cards: c.evidence_cards.map(card => {
      const e = get('assessment_evidence', card.evidence_id);
      const link = t.evidence_skill_links.find(r => r.evidence_id === e.evidence_id);
      const visibleAt = c.steps.find(s => s.refs.assessment_evidence?.includes(e.evidence_id)).scene_ref;
      return { id: e.evidence_id, visibleAt, copy: card.presentation_copy, source: e.source_type, activity: t.assessment_activities.find(a => a.activity_id === e.activity_id).activity_type, mode: e.verification_mode, raw: e.raw_evidence, skill: skills.find(s => s.skill_id === link.confirmed_skill_id), link: { suggestionSource: link.suggestion_source, confirmedBy: link.confirmed_by, status: link.confirmation_status }, observations: t.assessment_observations.filter(o => o.evidence_id === e.evidence_id).map(o => ({ id: o.observation_id, role: o.evaluator_role, text: o.observation_text, level: o.proposed_level })) };
    }),
    steps: c.steps.map(s => ({ scene: s.scene_ref, copy: s.presentation_copy,
      observations: (s.refs.assessment_observations ?? []).map(id => { const o = get('assessment_observations', id); return { id, evidenceId: o.evidence_id, role: o.evaluator_role, text: o.observation_text, level: o.proposed_level }; }),
      skills: (s.refs.evidence_decisions ?? []).map(id => { const d = get('evidence_decisions', id); return { id, skillId: d.skill_id, level: d.final_level, status: d.decision_status, reason: d.rationale.reason, observationIds: t.skill_decision_observations.filter(l => l.decision_id === id).map(l => l.observation_id) }; }),
      stages: (s.refs.stage_history ?? []).map(id => { const d = get('stage_history', id); return { id, stage: d.stage, result: d.result, reason: d.decision_reason_code, rationale: { human_rationale: d.rationale.human_rationale, coverage: d.rationale.coverage ?? null } }; }),
      finals: (s.refs.final_decisions ?? []).map(id => { const d = get('final_decisions', id); return { id, round: d.review_round, decision: d.decision, holdReason: d.hold_reason_code, rationale: { human_rationale: d.rationale.human_rationale }, plan: Array.isArray(d.resolution_plan) ? d.resolution_plan.map(p => ({ skill_id: p.skill_id, question: p.question })) : [] }; }),
      followups: (s.refs.targeted_followups ?? []).map(id => (() => { const f = get('targeted_followups', id); return { evidence_id: f.evidence_id, hold_decision_id: f.hold_decision_id, skill_id: f.skill_id, question: f.question, response_kind: f.response_kind }; })()),
      calibrations: (s.refs.calibration_reviews ?? []).map(id => { const r = get('calibration_reviews', id); return { id, triggers: r.trigger_codes, activityId: r.activity_id, rationale: r.rationale }; })
    }))
  }));
  const sceneDoc = read('docs/06_mission1_experience_specification.md');
  const stageNames = ['인력계획', '인재 정의', '채용 설계', '지원자 검증', '인재 확보', '업무 준비'];
  const scenes = [...sceneDoc.matchAll(/^### (M1-\d+)\. (.+)\n([\s\S]*?)(?=^### M1-|^## 4\.|$(?![\s\S]))/gm)].map(([, id, title, body]) => {
    const field = key => body.match(new RegExp(`^- \\*\\*${key}:\\*\\* (.+)$`, 'm'))?.[1] ?? '';
    const [stage, space] = field('Stage / Space').split(' / ');
    return { id, title, stage: stage === 'Mission 전환' ? 5 : stageNames.indexOf(stage), space, question: field('Core Question'), roles: field('Participants').split(', '), human: field('Human Layer'), interaction: field('Interaction'), nextQuestion: field('Next Question') };
  });
  if (scenes.length !== 25 || scenes.some(s => s.stage < 0)) throw Error('Scene contract mismatch');
  const first = entered('FIRST_INTERVIEW');
  const fcount = result => first.filter(r => r.result === result).length;
  const calibrationIds = new Set(t.calibration_reviews.filter(r => r.activity_id && t.assessment_activities.some(a => a.activity_id === r.activity_id && a.completed_at)).map(r => r.activity_id));
  const calibrationHours = t.activity_participants.filter(p => calibrationIds.has(p.activity_id)).reduce((n, p) => n + (Date.parse(p.participation_ended_at) - Date.parse(p.participation_started_at)) / 3600000, 0);
  return { datasetVersion: mapping.dataset_version, mappingVersion: mapping.mapping_version, manifestHash: mapping.baseline_manifest_sha256, observationEnd: manifest.observation_end, sourcePath: source, stages: stageNames, scenes, skills,
    workforcePlan: t.workforce_plan, funnel: t.funnel_plan.map((p, i) => ({ stage: p.stage, label: p.label, target: p.target_count, actual: counts[i] })),
    capacity: { initial: initial.person_hours, planned: plan.target_count, unit: plan.unit_effort_person_hours, demand: demand.demand_person_hours, gap: demand.person_hours, additional: sum(added), revised: initial.person_hours + sum(added), consumed: sum(t.capacity_assignments.filter(r => r.event_type === 'CONSUMED')), released: sum(t.capacity_assignments.filter(r => r.event_type === 'RELEASED')), reserved: sum(t.capacity_assignments.filter(r => r.event_type === 'RESERVED')), pool: initial.rationale.evaluator_count, decision: added[0].rationale, sourceIds: cap.map(r => r.capacity_event_id), calibrationCount: calibrationIds.size, calibrationHours },
    interview: { entered: first.length, advanced: fcount('ADVANCED'), failed: fcount('FAILED'), waiting: fcount('IN_PROGRESS'), withdrawn: fcount('WITHDRAWN') },
    outcomes: { offered: t.offers.length, accepted: t.offer_events.filter(r => r.event_type === 'ACCEPTED').length, declined: t.offer_events.filter(r => r.event_type === 'DECLINED').length, expired: t.offer_events.filter(r => r.event_type === 'EXPIRED').length, preJoinWithdrawal: t.offer_events.filter(r => r.event_type === 'PRE_JOIN_WITHDRAWAL').length, joined: uniq(joined, 'employee_id'), ready: uniq(ready, 'employee_id'), targetDateReady: uniq(ready.filter(r => r.effective_at.slice(0, 10) <= t.workforce_plan.target_date), 'employee_id'), gaps: t.onboarding_skill_gaps.length, tasks: t.onboarding_tasks.length },
    readyProof: ready.map(r => ({ id: r.workforce_event_id, effectiveAt: r.effective_at, confirmedAt: r.confirmed_at, confirmedBy: r.confirmed_by, reason: r.source_ref.human_rationale, tasks: t.onboarding_tasks.filter(task => r.source_ref.work_evidence_refs.includes(task.evidence_ref)).map(task => ({ id: task.task_id, action: task.work_evidence.performed_action, observedAt: task.work_evidence.observed_at, sourceRef: task.evidence_ref })) })),
    cases
  };
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const output = JSON.stringify(project(), null, 2) + '\n';
  const file = 'app/exploration/v2/view.json';
  if (process.argv.includes('--check')) { if (read(file) !== output) throw Error('Stale Mission 1 UI projection'); }
  else { let old; try { old = read(file); } catch {} if (old !== output) writeFileSync(path.join(root, file), output); }
  console.log('Mission 1 v1 presentation projection verified');
}
