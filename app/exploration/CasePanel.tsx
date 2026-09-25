"use client";

import { createContext, useContext, useEffect, useId, useRef, useState, type ReactNode } from "react";
import { forecastSupply, gap, mission, steps, type StepId } from "./model";
import talentProfile from "../../data/case/talent_profile.json";

type ContentCamera = { activeDisclosure: string | null; onOpen: (trigger: HTMLButtonElement, inner: HTMLDivElement, title: string) => void; onDismiss: () => void };
const ContentCameraContext = createContext<ContentCamera | null>(null);

function Disclosure({ title, children }: { title: string; children: ReactNode }) {
  const camera = useContext(ContentCameraContext);
  const [open, setOpen] = useState(false);
  const contentId = useId();
  const triggerRef = useRef<HTMLButtonElement>(null);
  const innerRef = useRef<HTMLDivElement>(null);
  function toggle() {
    const opening = !open;
    setOpen(opening);
    if (!opening) { camera?.onDismiss(); return; }
    window.requestAnimationFrame(() => {
      const trigger = triggerRef.current;
      const inner = innerRef.current;
      if (!trigger || !inner) return;
      if (camera) { camera.onOpen(trigger, inner, title); return; }
      const scrollBody = trigger.closest<HTMLElement>(".po-case-body");
      if (!scrollBody) return;
      const triggerRect = trigger.getBoundingClientRect();
      const bodyRect = scrollBody.getBoundingClientRect();
      const neededBelow = Math.min(inner.scrollHeight, 160);
      if (bodyRect.bottom - triggerRect.bottom >= neededBelow + 12) return;
      const top = scrollBody.scrollTop + triggerRect.top - bodyRect.top - 18;
      scrollBody.scrollTo({ top: Math.max(0, top), behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
    });
  }
  return <div className="po-disclosure" data-open={open} data-spotlight={camera?.activeDisclosure === title}>
    <button ref={triggerRef} type="button" className="po-disclosure-trigger" aria-expanded={open} aria-controls={contentId} onClick={toggle}><span aria-hidden="true">{open ? "▾" : "▸"}</span> {title}</button>
    <div id={contentId} className="po-disclosure-content" aria-hidden={!open} inert={!open}><div ref={innerRef} className="po-disclosure-inner">{children}</div></div>
  </div>;
}

type EvidenceType = "PUBLIC" | "INFERENCE" | "SYNTHETIC" | "ANALYSIS";
const evidenceLabels: Record<EvidenceType, string> = { PUBLIC: "공개자료", INFERENCE: "직무 해석", SYNTHETIC: "시나리오 가정", ANALYSIS: "데이터 분석" };
export function EvidenceBadge({ type }: { type: EvidenceType }) {
  return <span className={`po-evidence ${type.toLowerCase()}`}>{evidenceLabels[type]}</span>;
}

type Skill = (typeof talentProfile.skills)[number];
type Requirement = "MUST" | "LEARNABLE" | "PLUS";
const categories: Array<{ id: Requirement; label: string }> = [
  { id: "MUST", label: "Must Have" }, { id: "LEARNABLE", label: "Learnable" }, { id: "PLUS", label: "Plus" },
];

function TalentDeskContent() {
  const [category, setCategory] = useState<Requirement>("MUST");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const skills = talentProfile.skills.filter(skill => skill.requirement === category);
  const selected = talentProfile.skills.find(skill => skill.skill_id === selectedId) as Skill | undefined;
  const sources = selected?.source_reference.map(ref => talentProfile.sources.find(source => source.id === ref)).filter(source => source !== undefined) ?? [];
  return <>
    <section><h3>이번 단계에서 할 일</h3><p className="po-section-lead">앞서 확인한 부족 인력을 어떤 역량을 갖춘 사람으로 확보할지 정합니다. 먼저 업무 흐름을 보고, 필요한 Skill을 분류한 뒤 확인할 경험을 살펴보세요.</p></section>
    <section><h3>Talent Profile 요약</h3><EvidenceBadge type="SYNTHETIC" /> <EvidenceBadge type="INFERENCE" />
      <p>{talentProfile.summary}</p>
      <Disclosure title="업무 이해 · 공개자료와 직무 해석">
        <p><EvidenceBadge type="PUBLIC" /> 공개자료는 ML·최적화 기반 솔루션 개발, 구현·검증·적용과 협업 범위를 보여줍니다.</p>
        <ol className="po-job-flow">{talentProfile.job_context.map(item => <li key={item}>{item}</li>)}</ol>
        <p><EvidenceBadge type="INFERENCE" /> {talentProfile.job_context_note}</p>
        {talentProfile.sources.map(source => <p key={source.id}><a href={source.url} target="_blank" rel="noopener noreferrer">{source.publisher} · {source.title} ↗</a></p>)}
      </Disclosure>
    </section>
    <section><h3>필요한 Skill 정의</h3><p className="po-section-lead">Must Have는 처음부터 확인할 역량, Learnable은 입사 후 배울 수 있는 역량, Plus는 있으면 도움이 되는 경험입니다.</p><p className="po-muted">분류를 고른 뒤 Skill 하나를 눌러 정의·판단 이유·확인할 경험을 차례로 살펴보세요.</p>
      <div className="po-skill-categories" role="group" aria-label="Skill 분류">{categories.map(item => <button key={item.id} type="button" aria-pressed={category === item.id} onClick={() => { setCategory(item.id); setSelectedId(null); }}>{item.label}<small>{talentProfile.skills.filter(skill => skill.requirement === item.id).length}</small></button>)}</div>
      <p className="po-category-reason"><EvidenceBadge type="INFERENCE" /> {talentProfile.category_rationale[category]}</p>
      <div className="po-skill-list">{skills.map(skill => <button key={skill.skill_id} type="button" aria-pressed={selectedId === skill.skill_id} onClick={() => setSelectedId(selectedId === skill.skill_id ? null : skill.skill_id)}><span>{skill.name}</span><small>{categories.find(item => item.id === skill.requirement)?.label} · 상세 보기 →</small></button>)}</div>
      {selected && <div className="po-skill-detail" key={selected.skill_id}>
        <p className="po-skill-detail-label">{categories.find(item => item.id === selected.requirement)?.label} · {selected.skill_id}</p>
        <h4>{selected.name}</h4><h5>정의</h5><p>{selected.definition}</p>
        <Disclosure title={`왜 ${categories.find(item => item.id === selected.requirement)?.label}인가?`}><EvidenceBadge type="INFERENCE" /><p>{selected.reason}</p><p>{talentProfile.category_rationale[selected.requirement as Requirement]}</p></Disclosure>
        <Disclosure title="확인할 Evidence"><EvidenceBadge type={selected.evidence_type as EvidenceType} /><p>{selected.expected_evidence}</p><p className="po-muted">지원자의 실제 평가 결과가 아닌, 이 시나리오에서 확인하기로 정의한 경험입니다.</p></Disclosure>
        <Disclosure title="근거 보기"><p><EvidenceBadge type="INFERENCE" /> 분류와 확인 방식은 프로젝트의 직무 해석입니다. 근거 참조: {selected.evidence_refs.join(", ")}</p>{sources.length ? sources.map(source => <p key={source.id}><EvidenceBadge type="PUBLIC" /> <a href={source.url} target="_blank" rel="noopener noreferrer">{source.publisher} · {source.title} ↗</a><br /><span className="po-muted">{source.note}</span></p>) : <p>이 Skill을 직접 요구하는 공개자료는 연결하지 않았습니다.</p>}</Disclosure>
      </div>}
    </section>
    <section><h3>Target Candidate · 프로젝트 결정</h3><EvidenceBadge type="INFERENCE" /><p className="po-target-candidate">{talentProfile.target_candidate}</p><p className="po-muted">위 Skill 분류와 공개 직무 참고자료를 바탕으로 이 시나리오에서 정한 인재상입니다. 특정 회사의 내부 기준이 아닙니다.</p></section>
  </>;
}

function WorkforceJourney({ focus, spotlight, onAdvance }: { focus: number; spotlight: string | null; onAdvance: (next: number) => void }) {
  const supplyFormula = `${mission.current_fte} ${mission.confirmed_flow.map(flow => `${flow.fte >= 0 ? "+" : "−"} ${Math.abs(flow.fte)}`).join(" ")} = ${forecastSupply}`;
  return <>
    <section className="po-journey-section" data-journey-focus="1" data-current={spotlight === "journey-1"} tabIndex={-1}>
      <h3>01 · 지금 확인할 질문</h3><p className="po-question">{steps[0].question}</p>
      <p className="po-section-lead">요청한 목표 인력이 모두 신규 채용 인원은 아닙니다. 현재 인력에 확정된 이동을 반영한 뒤, 목표 시점에 얼마나 부족한지 계산합니다.</p>
      <p className="po-journey-route">인력 데이터 → 목표 시점 예상 인력 → 부족 인력 → 판단</p>
      {focus === 1 && <button className="po-journey-button" onClick={() => onAdvance(2)}>현재 인력과 확정된 이동 보기 →</button>}
    </section>
    {focus >= 2 && <section className="po-journey-section" data-journey-focus="2" data-current={spotlight === "journey-2"} tabIndex={-1}>
      <h3>02 · 계산에 사용할 인력 데이터</h3><EvidenceBadge type="SYNTHETIC" />
      <p className="po-section-lead">목표 인력은 업무에 필요한 전체 인력입니다. 전입은 다른 조직에서 오는 인력, 전출은 다른 조직으로 옮기는 인력입니다. FTE는 근무시간을 상근 인원으로 환산한 단위이며, 1 FTE는 상근 1명분입니다.</p>
      <p className="po-dates">현재 인력 기준일 {mission.baseline_date}<br />업무 수행 준비를 마쳐야 하는 날짜 {mission.target_ready_date}</p>
      <dl className="po-journey-facts"><div><dt>필요한 인력 · Demand</dt><dd>{mission.demand_fte} FTE</dd></div><div><dt>현재 인력 · Current Supply</dt><dd>{mission.current_fte} FTE</dd></div></dl>
      <table className="po-flow-table"><caption>목표 시점까지 확정된 인력 이동 · Confirmed Flow</caption><tbody>{mission.confirmed_flow.map(flow => <tr key={flow.date}><th scope="row">{flow.date} {flow.label}</th><td>{flow.fte > 0 ? "+" : ""}{flow.fte} FTE</td></tr>)}</tbody></table>
      {focus === 2 && <button className="po-journey-button" onClick={() => onAdvance(3)}>전입·전출을 반영해 예상 인력 계산 →</button>}
    </section>}
    {focus >= 3 && <section className="po-journey-section" data-journey-focus="3" data-current={spotlight === "journey-3"} tabIndex={-1}>
      <h3>03 · 목표 시점 예상 인력</h3><p className="po-section-lead">현재 인력에 확정 전입을 더하고 확정 전출을 뺍니다. 아직 확정되지 않은 채용은 이 계산에 넣지 않습니다.</p>
      <p className="po-formula">{supplyFormula} FTE</p>
      <p className="po-muted">계산 결과는 목표 날짜에 확보될 것으로 예상하는 인력(Forecast Supply)입니다. 신규 채용으로 확보할 인력은 아직 포함하지 않았습니다.</p>
      {focus === 3 && <button className="po-journey-button" onClick={() => onAdvance(4)}>필요한 인력과 비교해 부족 인력 계산 →</button>}
    </section>}
    {focus >= 4 && <section className="po-journey-section" data-journey-focus="4" data-current={spotlight === "journey-4"} tabIndex={-1}>
      <h3>04 · 목표 시점 부족 인력</h3><p className="po-section-lead">목표 날짜에 필요한 인력에서 같은 날짜의 예상 인력을 뺍니다. 그 차이가 추가로 확보해야 할 부족 인력(Gap)입니다.</p><dl className="po-metrics"><div><dt>필요한 인력<br />Demand</dt><dd>{mission.demand_fte}<small> FTE</small></dd></div><div><dt>예상 인력<br />Forecast Supply</dt><dd>{forecastSupply}<small> FTE</small></dd></div><div><dt>부족 인력<br />Gap</dt><dd>{gap}<small> FTE</small></dd></div></dl>
      <p className="po-formula">{mission.demand_fte} − {forecastSupply} = {gap} FTE</p>
      {focus === 4 && <button className="po-journey-button" onClick={() => onAdvance(5)}>왜 예상 인력으로 비교했는지 보기 →</button>}
    </section>}
    {focus >= 5 && <section className="po-journey-section" data-journey-focus="5" data-current={spotlight === "journey-5"} tabIndex={-1}>
      <h3>05 · 판단 근거와 결정</h3><EvidenceBadge type="INFERENCE" /><p className="po-section-lead">목표 날짜에 필요한 인력과 그날 확보될 예상 인력을 비교해야 합니다.</p><p>{steps[0].reasoning}</p>
      <p><b>결정:</b> {steps[0].decision}</p>
      <Disclosure title="대안과 근거 보기"><ul><li><b>신입 외부채용:</b> 기존 숙련 인력이 신입의 학습을 지원할 수 있고, 업무에 익숙해질 기간 6개월을 확보할 수 있어 선택했습니다.</li><li><b>경력채용:</b> 입사 직후 혼자 업무를 수행해야 하는 상황은 아니므로, 이번 시나리오의 기본 방향으로 선택하지 않았습니다.</li><li><b>내부이동:</b> 이미 확정된 전입·전출을 반영해도 인력이 부족합니다.</li><li><b>내부 육성·외부 인력 활용:</b> 기존 직원의 역량을 키우거나 외부 인력의 도움을 받는 방법도 검토 대상입니다. 세부 비교 근거는 아직 준비 중입니다.</li></ul></Disclosure>
      {focus === 5 && <button className="po-journey-button" onClick={() => onAdvance(6)}>확보할 인재에 대한 다음 질문 보기 →</button>}
    </section>}
    {focus >= 6 && <section className="po-journey-section" data-journey-focus="6" data-current={spotlight === "journey-6"} tabIndex={-1}>
      <h3>06 · 다음 의사결정</h3><p className="po-question">{steps[0].nextQuestion}</p>
      <p className="po-section-lead">이제 채용할 사람이 갖춰야 할 역량을 정합니다. Talent Desk에서 업무 내용을 살펴보고, 지원자의 어떤 경험을 통해 역량을 확인할지 알아보세요.</p>
    </section>}
  </>;
}

export default function CasePanel({ id, reviewed, guidance, onNext, onPrevious }: {
  id: StepId; reviewed: boolean; guidance: boolean; onNext: () => void; onPrevious?: () => void;
}) {
  const [shownId, setShownId] = useState(id);
  const [phase, setPhase] = useState<"enter" | "exit" | "idle">("enter");
  const [workforceFocus, setWorkforceFocus] = useState(1);
  const workforceFocusRef = useRef(1);
  const shownIdRef = useRef(id);
  const bodyRef = useRef<HTMLDivElement>(null);
  const cameraFrameRef = useRef(0);
  const [spotlight, setSpotlight] = useState<string | null>(id === "workforce" ? "journey-1" : "question");
  const cancelContentCamera = () => {
    window.cancelAnimationFrame(cameraFrameRef.current);
    setSpotlight(null);
  };
  const moveTo = (target: HTMLElement, onArrive: () => void) => {
    const body = bodyRef.current;
    if (!body || body.scrollHeight <= body.clientHeight) { onArrive(); return; }
    const bodyRect = body.getBoundingClientRect();
    const targetRect = target.getBoundingClientRect();
    const desiredOffset = target.matches(".po-disclosure") || targetRect.height >= bodyRect.height * .78 ? 18 : Math.max(18, (bodyRect.height - targetRect.height) / 2);
    const destination = Math.max(0, Math.min(body.scrollHeight - body.clientHeight, body.scrollTop + targetRect.top - bodyRect.top - desiredOffset));
    const start = body.scrollTop;
    if (Math.abs(destination - start) < 4) { onArrive(); return; }
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { body.scrollTop = destination; onArrive(); return; }
    const startTime = performance.now();
    const animate = (now: number) => {
      const progress = Math.min(1, (now - startTime) / 380);
      body.scrollTop = start + (destination - start) * (1 - Math.pow(1 - progress, 3));
      if (progress < 1) cameraFrameRef.current = window.requestAnimationFrame(animate);
      else onArrive();
    };
    cameraFrameRef.current = window.requestAnimationFrame(animate);
  };
  const advanceWorkforce = (next: number) => {
    window.cancelAnimationFrame(cameraFrameRef.current);
    workforceFocusRef.current = next;
    setWorkforceFocus(next);
    setSpotlight(null);
    cameraFrameRef.current = window.requestAnimationFrame(() => {
      const target = bodyRef.current?.querySelector<HTMLElement>(`[data-journey-focus="${next}"]`);
      if (target) { target.focus({ preventScroll: true }); moveTo(target, () => setSpotlight(`journey-${next}`)); }
    });
  };
  const focusDisclosure = (trigger: HTMLButtonElement, inner: HTMLDivElement, title: string) => {
    cancelContentCamera();
    const target = trigger.closest<HTMLElement>(".po-disclosure");
    if (!target || !inner) return;
    // Anchor the disclosure heading so its expanding height cannot shift the destination.
    cameraFrameRef.current = window.requestAnimationFrame(() => {
      moveTo(target, () => setSpotlight(title));
    });
  };
  useEffect(() => {
    if (id === shownIdRef.current) return;
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const timer = window.setTimeout(() => {
      shownIdRef.current = id;
      setShownId(id);
      setSpotlight(id === "workforce" ? `journey-${workforceFocusRef.current}` : "question");
      setPhase(reducedMotion ? "idle" : "enter");
    }, reducedMotion ? 0 : 135);
    return () => window.clearTimeout(timer);
  }, [id]);
  useEffect(() => {
    if (phase !== "enter") return;
    const timer = window.setTimeout(() => setPhase("idle"), guidance ? 180 : 240);
    return () => window.clearTimeout(timer);
  }, [phase, guidance]);
  const step = steps.find(item => item.id === shownId)!;
  const activePhase = id === shownId ? phase : "exit";
  const index = steps.indexOf(step);
  const headingRef = useRef<HTMLHeadingElement>(null);
  useEffect(() => { headingRef.current?.focus({ preventScroll: true }); }, [shownId]);
  useEffect(() => {
    const body = bodyRef.current;
    if (!body) return;
    const stop = () => { window.cancelAnimationFrame(cameraFrameRef.current); window.requestAnimationFrame(() => setSpotlight(null)); };
    body.addEventListener("wheel", stop, { passive: true });
    body.addEventListener("touchstart", stop, { passive: true });
    body.addEventListener("keydown", stop);
    return () => { body.removeEventListener("wheel", stop); body.removeEventListener("touchstart", stop); body.removeEventListener("keydown", stop); window.cancelAnimationFrame(cameraFrameRef.current); };
  }, [shownId]);
  return <article className="win po-case" aria-labelledby="case-title" data-step={shownId} data-guidance={guidance}>
    <ContentCameraContext.Provider value={{ activeDisclosure: spotlight, onOpen: focusDisclosure, onDismiss: cancelContentCamera }}><div key={shownId} className="po-case-content" data-phase={activePhase} inert={activePhase === "exit"}>
    <div className="win-bar"><span>MISSION 01 · STEP {String(index + 1).padStart(2, "0")}</span><span>{reviewed ? "✓ 확인함" : "현재 단계"}</span></div>
    <div ref={bodyRef} className="po-case-body" data-spotlight={spotlight} onPointerDownCapture={() => window.cancelAnimationFrame(cameraFrameRef.current)}>
      <h2 id="case-title" ref={headingRef} tabIndex={-1}>{step.title}</h2>
      {shownId === "workforce" ? <WorkforceJourney focus={workforceFocus} spotlight={spotlight} onAdvance={advanceWorkforce} /> : <>
        <section data-content-target="question" data-current={spotlight === "question"}><h3>이번 단계의 핵심 질문</h3><p className="po-question">{step.question}</p>{shownId === "talent" ? <p className="po-muted">아래에서 업무 내용과 Skill 분류를 살펴보고, Skill을 선택해 판단 근거를 확인하세요.</p> : <p className="po-muted">아래에서 관련 정보와 판단 과정을 확인한 뒤 다음 단계로 이어가세요.</p>}</section>
        {shownId === "talent" ? <TalentDeskContent /> : <>
          <section><h3>데이터와 근거</h3><EvidenceBadge type="SYNTHETIC" /><p>{step.data}</p><Disclosure title="데이터 확인"><p>{step.reference}</p><p>현재 표시 내용은 제품 문서에 확정된 시나리오와 설명입니다. 공개 근거와 결과 데이터는 추가 연결 예정입니다.</p></Disclosure>{step.pending && <p className="po-pending">{step.pending}</p>}</section>
          <section><h3>판단 과정</h3><p>{step.reasoning}</p><Disclosure title="판단 근거 보기"><EvidenceBadge type="INFERENCE" /><p>{step.reasoning}</p><p>참조: {step.reference}</p></Disclosure></section>
          <section><h3>결정</h3><p>{step.decision}</p><Disclosure title="대안과 근거 보기"><p>이 단계의 상세 대안 비교는 아직 연결되지 않았습니다. 문서에 확정된 원칙과 준비 상태만 제공합니다.</p><p>참조: {step.reference}</p></Disclosure></section>
        </>}
      </>}
    </div>
      <section className="po-next"><h3>{shownId === "workforce" && workforceFocus < 6 ? "이어서 확인하기" : "다음 단계"}</h3><p>{shownId === "workforce" && workforceFocus < 6 ? "본문의 화살표 버튼을 누르면 다음 내용을 확인할 수 있습니다. 이전 내용은 위로 스크롤해 다시 읽을 수 있습니다." : step.nextQuestion}</p>
        {(shownId !== "workforce" || workforceFocus >= 6) && <button className="po-primary" onClick={onNext}>{steps[index + 1] ? `${steps[index + 1].title}로 이동 →` : "확인 완료 · Mission Board로 →"}</button>}
        {onPrevious && <button className="po-text-button" onClick={onPrevious}>← 이전 단계</button>}
      </section>
    </div></ContentCameraContext.Provider>
  </article>;
}
