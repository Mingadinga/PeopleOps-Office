import mission from "../../data/case/mission1.json";

export { mission };
export type StepId = "workforce" | "talent" | "attraction" | "operations" | "onboarding" | "kpi";
export type Destination = StepId | "board" | "lab";
export type ExplorationStatus = "CURRENT" | "REVIEWED" | "UPCOMING";
export const steps = mission.steps as Array<(typeof mission.steps)[number] & { id: StepId }>;
export const forecastSupply = mission.current_fte + mission.confirmed_flow.reduce((sum, flow) => sum + flow.fte, 0);
export const gap = mission.demand_fte - forecastSupply;
export const statusLabels: Record<ExplorationStatus, string> = {
  CURRENT: "현재 단계", REVIEWED: "✓ 확인함", UPCOMING: "살펴볼 단계",
};

// Office layout is presentation data, independent of Company and its simulation IDs.
export const rooms: Array<{ id: Exclude<Destination, "board" | "kpi">; name: string; icon: string; x: number; y: number; role: string; question: string }> = [
  { id: "workforce", name: "인력계획실", icon: "▦", x: 42, y: 52, role: "Workforce Planner", question: steps[0].question },
  { id: "talent", name: "Talent Desk", icon: "◇", x: 344, y: 52, role: "Talent Partner", question: steps[1].question },
  { id: "attraction", name: "채용전략실", icon: "↗", x: 646, y: 52, role: "Recruiter", question: steps[2].question },
  { id: "operations", name: "채용운영실", icon: "☷", x: 42, y: 364, role: "Recruiting Operator", question: steps[3].question },
  { id: "onboarding", name: "Onboarding", icon: "✿", x: 344, y: 364, role: "People Partner", question: steps[4].question },
  { id: "lab", name: "Data Lab", icon: "⌁", x: 646, y: 364, role: "People Analyst", question: "채용 데이터에서 무엇을 확인하고 개선할 것인가?" },
];

export type NavigationState = {
  destination: Destination;
  lastStep: StepId;
  reviewed: StepId[];
  started: boolean;
  intro: boolean;
  briefing: "request" | "goal" | null;
  guidance: boolean;
  cameraRevision: number;
};
export const initialNavigation: NavigationState = {
  destination: "board", lastStep: "workforce", reviewed: [], started: false,
  intro: true, briefing: null, guidance: false, cameraRevision: 0,
};
export type NavigationAction =
  | { type: "start" }
  | { type: "confirmRequest" }
  | { type: "beginPlanning" }
  | { type: "select"; destination: Destination }
  | { type: "next"; step: StepId }
  | { type: "dismissIntro" }
  | { type: "dismissGuidance" };

export function navigationReducer(state: NavigationState, action: NavigationAction): NavigationState {
  if (action.type === "dismissIntro") return { ...state, intro: false };
  if (action.type === "dismissGuidance") return { ...state, guidance: false };
  if (action.type === "start") return { ...state, intro: false, briefing: "request", destination: "board", guidance: false };
  if (action.type === "confirmRequest") return { ...state, briefing: "goal" };
  if (action.type === "beginPlanning") return {
    ...state, destination: "workforce", lastStep: "workforce", started: true,
    intro: false, briefing: null, guidance: true, cameraRevision: state.cameraRevision + 1,
  };
  if (action.type === "next") {
    const index = steps.findIndex(step => step.id === action.step);
    if (state.destination !== action.step || index < 0) return state;
    const destination = steps[index + 1]?.id ?? "board";
    return {
      ...state, briefing: null, destination, lastStep: destination === "board" ? action.step : destination,
      reviewed: state.reviewed.includes(action.step) ? state.reviewed : [...state.reviewed, action.step],
      guidance: false, cameraRevision: state.cameraRevision + 1,
    };
  }
  const isStep = steps.some(step => step.id === action.destination);
  return {
    ...state, briefing: null, destination: action.destination, lastStep: isStep ? action.destination as StepId : state.lastStep,
    started: state.started || isStep, intro: false, guidance: false, cameraRevision: state.cameraRevision + 1,
  };
}

export function stepStatus(id: StepId, state: NavigationState): ExplorationStatus {
  return state.destination === id ? "CURRENT" : state.reviewed.includes(id) ? "REVIEWED" : "UPCOMING";
}

export function nextStepId(state: NavigationState): StepId | undefined {
  const index = steps.findIndex(step => step.id === state.destination);
  return index < 0 ? undefined : steps[index + 1]?.id;
}
