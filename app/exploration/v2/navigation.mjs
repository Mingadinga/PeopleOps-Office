export const STORAGE_KEY = 'peopleops-m1-v1-mapping1-navigation';
export const initial = { scene: 0, frontier: 0, started: false, done: false, caseId: '', room: '' };
export function sanitize(value) {
  if (!value || typeof value !== 'object') return { ...initial };
  const frontier = Number.isInteger(value.frontier) ? Math.max(0, Math.min(24, value.frontier)) : 0;
  const scene = Number.isInteger(value.scene) ? Math.max(0, Math.min(frontier, value.scene)) : 0;
  return { scene, frontier, started: value.started === true, done: value.done === true && frontier === 24, caseId: typeof value.caseId === 'string' ? value.caseId : '', room: typeof value.room === 'string' ? value.room : '' };
}
export function move(state, scene) {
  if (!Number.isInteger(scene) || scene < 0 || scene > state.frontier) return state;
  return { ...state, scene, caseId: '', room: '' };
}
export function advance(state) {
  if (!state.started) return state;
  if (state.scene === 24) return { ...state, done: true };
  const next = state.scene + 1;
  return { ...state, scene: next, frontier: Math.max(state.frontier, next), caseId: '', room: '' };
}
export function restore(value, search) {
  const state = sanitize(value);
  const query = new URLSearchParams(search);
  const match = /^M1-(\d{2})$/.exec(query.get('scene') ?? '');
  if (match && state.started) state.scene = Math.min(state.frontier, Math.max(0, Math.min(24, Number(match[1]) - 1)));
  state.caseId = query.get('case') ?? state.caseId;
  return state;
}
