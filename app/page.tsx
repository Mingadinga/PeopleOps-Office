"use client";

import { useEffect, useReducer } from "react";
import OfficeWorld from "./game/OfficeWorld";
import CasePanel from "./exploration/CasePanel";
import MissionIntro from "./exploration/MissionIntro";
import PeopleOpsHeader from "./exploration/PeopleOpsHeader";
import MissionBoard from "./exploration/MissionBoard";
import MissionBriefing from "./exploration/MissionBriefing";
import { initialNavigation, navigationReducer, steps, stepStatus, statusLabels, type Destination } from "./exploration/model";

export default function Home() {
  const [state, dispatch] = useReducer(navigationReducer, initialNavigation);
  const select = (destination: Destination) => dispatch({ type: "select", destination });
  const step = steps.find(item => item.id === state.destination);
  const index = step ? steps.indexOf(step) : -1;

  useEffect(() => {
    if (!state.guidance) return;
    const timer = window.setTimeout(() => dispatch({ type: "dismissGuidance" }), 4500);
    return () => window.clearTimeout(timer);
  }, [state.guidance]);

  return <main className={`po-app ${state.intro ? "intro-visible" : ""}`}>
    <div className="po-shell" inert={state.intro}>
      <PeopleOpsHeader state={state} onSelect={select} />
      <div className="po-heading"><div><p className="po-kicker">HR WORKSPACE · 근거를 따라, 다음 의사결정으로.</p><h1>{step?.question ?? (state.destination === "lab" ? "채용 데이터에서 무엇을 확인하고 개선할 것인가?" : "인력 확보의 과정을 따라가 보세요.")}</h1></div><p>문제 확인 → 근거 탐색 → 판단 이해</p></div>
      <div className="po-workspace" id="office">
        <div className="po-map-column">
          <OfficeWorld state={state} onSelect={select} />
          <details className="po-step-details"><summary>전체 단계 보기</summary><nav className="po-step-nav" aria-label="Mission 01 단계 선택">{steps.map((item, i) => <button key={item.id} data-status={stepStatus(item.id, state)} aria-current={step?.id === item.id ? "step" : undefined} onClick={() => select(item.id)}><span>{i + 1}. {item.title}</span><small>{statusLabels[stepStatus(item.id, state)]}{step?.id === item.id && state.reviewed.includes(item.id) ? " · ✓" : ""}</small></button>)}</nav><p className="po-map-note">확인 표시는 탐색 이력입니다. 단계 선택으로 HR 결과가 바뀌지 않습니다.</p></details>
        </div>
        {state.briefing ? <MissionBriefing stage={state.briefing} onConfirm={() => dispatch({ type: "confirmRequest" })} onBegin={() => dispatch({ type: "beginPlanning" })} />
          : step ? <CasePanel id={step.id} reviewed={state.reviewed.includes(step.id)} guidance={state.guidance} onNext={() => dispatch({ type: "next", step: step.id })} onPrevious={index > 0 ? () => select(steps[index - 1].id) : undefined} />
          : state.destination === "lab" ? <section className="win po-case" aria-labelledby="lab-title"><div className="win-bar">MISSION 02 · Data Lab</div><div className="po-case-body"><p className="po-kicker">분석 WORKSPACE · 준비 중</p><h2 id="lab-title">다음 채용을 위한 질문을 준비합니다.</h2><p>Mission 1의 KPI를 검토하고 데이터를 분석해, 개선안을 다음 채용전략으로 연결하는 공간입니다.</p><p>분석 목표 → 데이터 확인 → Python / Pandas → 해석 → 가설 → 추가 분석 → 개선안</p><p className="po-pending">실제 분석 Workspace와 EDA 결과는 아직 제공하지 않습니다.</p><button className="po-primary" onClick={() => select(state.lastStep)}>Mission 01로 돌아가기 →</button></div></section>
          : <MissionBoard state={state} onSelect={select} onStart={() => dispatch({ type: "start" })} />}
      </div>
      <footer className="po-footer">PeopleOps Office · 시나리오 기반 HR 탐색<br />원본 Pixel Office: 갓생맘 🎀 · <a href="https://www.instagram.com/godseng.mom/" target="_blank" rel="noreferrer">@godseng.mom</a><br />© godseng.mom · 자유롭게 쓰되 무단 재판매 금지</footer>
    </div>
    {state.intro && <MissionIntro onStart={() => dispatch({ type: "start" })} onClose={() => dispatch({ type: "dismissIntro" })} />}
  </main>;
}
