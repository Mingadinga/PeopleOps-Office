import { mission } from "./model";

const questions = [
  "현재 인력은 충분한가?",
  "어떤 인재가 필요한가?",
  "필요한 인재에게 직무를 어떻게 알리고 지원을 유도할 것인가?",
  "어떤 방식으로 역량을 검증할 것인가?",
  "입사한 사람이 목표 날짜까지 업무를 수행할 준비를 마쳤는가?",
];

export default function MissionBriefing({ stage, onConfirm, onBegin }: {
  stage: "request" | "goal"; onConfirm: () => void; onBegin: () => void;
}) {
  if (stage === "request") return <section className="win po-briefing po-request" aria-labelledby="request-title">
    <div className="win-bar"><span>MISSION 01 · 새로운 업무 요청</span><span>접수됨</span></div>
    <div className="po-briefing-body">
      <p className="po-request-icon" aria-hidden="true">▤</p>
      <p className="po-kicker">WORKFORCE REQUEST</p>
      <h2 id="request-title">새로운 인력 요청이 도착했습니다!</h2>
      <p className="po-request-summary">가상의 AI/ML 조직에서 Machine Learning Engineer 인력 확보 요청이 접수되었습니다.</p>
      <span className="po-evidence synthetic">시나리오 가정</span>
      <p className="po-muted">아래 요청은 가상 시나리오이며, 실제 회사의 내부 조직·인력 데이터가 아닙니다.</p>
      <dl className="po-request-fields">
        <div><dt>직무</dt><dd>Machine Learning Engineer</dd></div>
        <div><dt>목표 인력 · Demand</dt><dd>{mission.demand_fte} FTE</dd></div>
        <div><dt>업무 수행 준비 목표일</dt><dd>{mission.target_ready_date.slice(0, 7)}</dd></div>
        <div><dt>요청 배경</dt><dd>사업 수행을 위한 ML 역량 확보</dd></div>
      </dl>
      <p className="po-request-note">목표 인력은 신규 채용 인원이 아니라 업무에 필요한 전체 인력입니다. 현재 인력과 확정된 이동을 확인한 뒤, 추가로 필요한 인력을 계산합니다.</p>
      <button className="po-primary" onClick={onConfirm} autoFocus>요청서 확인 →</button>
    </div>
  </section>;

  return <section className="win po-briefing" aria-labelledby="briefing-title">
    <div className="win-bar"><span>MISSION 01 · GOAL BRIEFING</span><span>요청서 확인함</span></div>
    <div className="po-briefing-body">
      <p className="po-kicker">이번 Mission의 질문</p>
      <h2 id="briefing-title">인력 요청을 어떻게 확인하고 실행할까요?</h2>
      <ol className="po-goal-questions">{questions.map((question, index) => <li key={question}><span>{String(index + 1).padStart(2, "0")}</span>{question}</li>)}</ol>
      <p className="po-muted">각 단계에서 데이터를 확인하고 판단 근거를 살펴봅니다.</p>
      <button className="po-primary" onClick={onBegin} autoFocus>인력계획 시작 →</button>
    </div>
  </section>;
}
