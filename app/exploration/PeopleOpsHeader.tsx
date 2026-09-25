import { steps, type Destination, type NavigationState } from "./model";

export default function PeopleOpsHeader({ state, onSelect }: { state: NavigationState; onSelect: (destination: Destination) => void }) {
  const index = steps.findIndex(step => step.id === state.destination);
  const isLab = state.destination === "lab";
  return <header className="po-header">
    <a className="po-brand" href="#office" onClick={event => { event.preventDefault(); onSelect(state.lastStep); }}><span>P</span>PeopleOps Office</a>
    <nav aria-label="주요 탐색">
      {([{ label: "Office", destination: state.lastStep, active: index >= 0 && state.destination !== "kpi" }, { label: "Mission", destination: "board", active: state.destination === "board" }, { label: "Data Lab", destination: "lab", active: isLab }, { label: "KPI", destination: "kpi", active: state.destination === "kpi" }] as const).map(item =>
        <button key={item.label} aria-current={item.active ? "page" : undefined} onClick={() => onSelect(item.destination)}>{item.label}</button>)}
    </nav>
    <div className="po-location" aria-live="polite"><strong>{isLab ? "MISSION 02 · 데이터 기반 개선" : "MISSION 01 · ML Engineer 인력 확보"}</strong><span>{index >= 0 ? `${steps[index].title} · ${index + 1} / 6 단계 탐색` : isLab ? "Data Lab · 준비 중" : "Mission Board · 탐색 안내"}</span></div>
  </header>;
}
