import data from './view.json';
import { copy, label } from './labels';
type Case = typeof data.cases[number];
function Reference({ ids }: { ids: string[] }) { return <details className="m1-reference"><summary>원본 기록 ID</summary>{ids.map(id => <code key={id}>{id}</code>)}</details>; }
export default function RepresentativeCase({ item, scene }: { item: Case; scene: string }) {
  const steps = item.steps.filter(s => s.scene <= scene);
  const current = steps.at(-1);
  const cards = item.cards.filter(c => c.visibleAt <= scene);
  return <section className="m1-case-trace" data-case={item.candidateId}>
    <h3>{item.question}</h3>
    <p className="m1-message">{copy(item.message)}</p>
    <p>{copy(current?.copy ?? '')}</p>
    <details><summary>사례 상세 · 기준 Dataset</summary><p>{item.candidateId} / {item.applicationId} · v1 · {item.skill.skill_name}</p><p>합성 근거와 합성 사람 판단의 기록입니다. 지원자 비교나 순위가 아닙니다.</p></details>
    <h4>확인한 근거</h4>
    <div className="m1-evidence-list">{cards.map(card => <article key={card.id} className="m1-evidence-card" data-evidence={card.id}>
      <header><b>{label(card.source === 'APPLICATION_RESPONSE' ? card.source : card.activity)}</b><span className="po-evidence">{label(card.mode)}</span></header>
      <p className="m1-skill">{card.skill.skill_name}</p><p>{copy(card.copy)}</p>
      <details><summary>원자료와 사람의 관찰 보기</summary>
        <blockquote>{card.raw.response}</blockquote>{card.raw.action && <p>수행: {card.raw.action}</p>}
        {card.raw.revision && <p>재확인: {card.raw.revision}</p>}
        <p className="m1-note">역량 연결: 사람이 확인한 연결 · 이 기록은 AI의 수준 평가가 아닙니다.</p>
        {card.observations.map(o => <div className="m1-observation" key={o.id}><b>{label(o.role)} · {label(o.level)}</b><p>{o.text}</p></div>)}
        <Reference ids={[card.id, ...card.observations.map(o => o.id)]} />
      </details>
    </article>)}</div>
    <h4>판단 근거 보기</h4>
    <p className="m1-note">근거 → 사람의 관찰 → 역량별 판단 → 전형 / 최종 판단</p>
    <ol className="m1-trace">{steps.map(step => <li key={step.scene} data-trace-scene={step.scene}>
      <b>{sceneTitlesForTrace(step.scene)}</b><p>{copy(step.copy)}</p>
      {step.observations.length > 0 && <details><summary>기록된 관찰 {step.observations.length}건</summary>{step.observations.map(o => <p key={o.id}>{label(o.role)}: {label(o.level)} — {o.text}</p>)}</details>}
      {step.calibrations.filter(c => c.activityId).map(c => <details key={c.id}><summary>평가 조정 · 해석 차이 확인</summary>{item.id === 'CASE_A' && <p>이 회의는 다른 역량의 해석 차이를 다룹니다. Skill02 미관찰 때문에 발생한 회의가 아닙니다.</p>}<p>동일 근거의 평가자 해석 차이 또는 직접 근거의 충돌을 검토했습니다. 아래 역량별 판단에 합의 여부가 남습니다.</p><p>{typeof c.rationale === 'string' ? copy(c.rationale) : JSON.stringify(c.rationale)}</p><Reference ids={[c.id, c.activityId]} /></details>)}
      {step.skills.map(s => <div key={s.id} className="m1-record"><b>{label(s.status)} · {label(s.level || 'NOT_OBSERVED')}</b><p>{copy(s.reason)}</p><Reference ids={[s.id, ...s.observationIds]} /></div>)}
      {step.stages.map(s => <div key={s.id} className="m1-record"><b>{label(s.stage)} · {s.reason === 'EVIDENCE_PENDING' ? label(s.reason) : label(s.result)}</b><p>{copy(s.rationale.human_rationale)}</p>{s.rationale.coverage && <ul>{Object.entries(s.rationale.coverage).map(([skill, status]) => <li key={skill}>{data.skills.find(k => k.skill_id === skill)?.skill_name}: {status.decisionable ? '직접 근거로 판단 가능' : '직접 근거로 판단 불가'}</li>)}</ul>}<Reference ids={[s.id]} /></div>)}
      {step.finals.map(f => <div key={f.id} className="m1-record" data-final={f.decision}><b>{label(f.round)} · {label(f.decision)}</b>{f.holdReason && <p>보류 이유: {label(f.holdReason)}</p>}<p>{copy(f.rationale.human_rationale)}</p>{f.plan.map((p, i) => <p key={i}>추가 확인 계획: {p.question.split(' 대상:')[0]}</p>)}<Reference ids={[f.id]} /></div>)}
      {step.followups.map(f => <div key={f.evidence_id} className="m1-record"><b>추가 확인 · {label(f.response_kind)}</b><p>{f.question.split(' 대상:')[0]}</p><Reference ids={[f.hold_decision_id, f.evidence_id]} /></div>)}
    </li>)}</ol>
    {(scene >= 'M1-19' || item.id === 'CASE_A' && scene >= 'M1-15') && <aside className="m1-caveat">{item.caveats.filter(c => !c.includes('EXPIRED') || scene >= 'M1-20').map(c => <p key={c}>{copy(c)}</p>)}</aside>}
  </section>;
}
function sceneTitlesForTrace(id: string) { return ({ 'M1-10': '지원서에서 경험 발견', 'M1-14': '직접 근거와 관찰', 'M1-15': '1차 판단', 'M1-16': '행동 근거 확인', 'M1-17': '최종 검토와 확인 계획', 'M1-18': '필요 근거 추가 확인', 'M1-19': '재검토' } as Record<string, string>)[id] ?? id; }
