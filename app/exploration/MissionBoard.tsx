import { statusLabels, steps, stepStatus, type Destination, type NavigationState } from "./model";

export default function MissionBoard({ state, onSelect, onStart }: { state: NavigationState; onSelect: (id: Destination) => void; onStart: () => void }) {
  return <section className="win po-board-panel" aria-labelledby="board-title">
    <div className="win-bar">Mission Board</div><div className="po-case-body">
      <p className="po-kicker">문제에서 다음 의사결정까지</p><h2 id="board-title">인력 확보의 과정을 따라가 보세요.</h2>
      <p>공간을 선택하면 그 단계의 질문과 판단 근거를 살펴볼 수 있습니다. 원하는 단계부터 열어도 됩니다.</p>
      <h3>MISSION 01 · ML Engineer 인력 확보</h3>
      <ol className="po-step-list">{steps.map((step, index) => <li key={step.id}><button onClick={() => onSelect(step.id)}><span>{String(index + 1).padStart(2, "0")}</span><b>{step.title}</b><small>{statusLabels[stepStatus(step.id, state)]}</small></button></li>)}</ol>
      <button className="po-primary" onClick={state.started ? () => onSelect(state.lastStep) : onStart}>{state.started ? "이어서 탐색하기 →" : "Mission 시작 →"}</button>
      <div className="po-future"><h3>MISSION 02 · 데이터 기반 개선</h3><p>Mission 1 데이터 → 분석 → 개선 → 다음 채용</p><p className="po-muted">Data Lab의 분석 Workspace는 준비 중입니다.</p><button className="po-text-button" onClick={() => onSelect("lab")}>Data Lab 안내 보기 →</button></div>
    </div>
  </section>;
}
