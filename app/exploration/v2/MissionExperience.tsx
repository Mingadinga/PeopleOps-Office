'use client';
import { useEffect, useRef, useState, type CSSProperties } from 'react';
import MissionIntro from '../MissionIntro';
import data from './view.json';
import { advance, initial, move, restore, STORAGE_KEY } from './navigation.mjs';
import { copy, sceneTitles } from './labels';
import RepresentativeCase from './RepresentativeCase';
import SceneContent from './SceneContent';

const rooms = ['인력계획실', '채용전략실', '채용운영실', '평가회의실', '면접실', '업무공간', '데이터랩'];
const think: Record<string, string> = { 'M1-02': '현재 인원만으로 목표일의 공급을 판단해도 될까요?', 'M1-09': '면접 계획 인원은 선발 정원일까요?', 'M1-12': '면접 수요가 계획을 넘으면 무엇을 바꿔야 할까요?', 'M1-15': '근거 미관찰은 역량 부족과 같은 뜻일까요?', 'M1-19': '추가 확인 후에도 필수 근거가 없다면 어떻게 할까요?', 'M1-23': '입사일이 지나면 업무 준비가 완료된 것일까요?' };
const physicalRoom = (space: string) => rooms.includes(space) ? space : space.includes('온라인') ? '면접실' : space.includes('지원자') ? '채용운영실' : '인력계획실';

function StoredReveal({ text }: { text: string }) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    const skip = () => { if (media.matches) setCount(text.length); };
    const timer = window.setInterval(() => setCount(n => Math.min(text.length, n + 4)), 20);
    skip(); media.addEventListener('change', skip);
    return () => { clearInterval(timer); media.removeEventListener('change', skip); };
  }, [text]);
  return <div className="m1-reveal"><div><small>저장된 v1 기록 · 단계별 표시</small>{count < text.length && <button onClick={() => setCount(text.length)}>전체 표시</button>}</div><p aria-hidden="true">{text.slice(0, count)}{count < text.length && <span className="m1-caret">▌</span>}</p><p className="m1-sr">{text}</p></div>;
}
function PixelPerson({ role, index }: { role: string; index: number }) { return <div className="m1-person"><span className="ag f-down" aria-hidden="true" style={{ '--hair': '#563d50', '--shirt': ['#c9b8ff', '#b8f0dd', '#ffb9d9', '#ffe49a'][index % 4], '--skin': '#ffdcc4' } as CSSProperties}><span className="ag-body"><i className="p-shadow" /><i className="p-leg l" /><i className="p-leg r" /><i className="p-torso" /><i className="p-arm l" /><i className="p-arm r" /><i className="p-head"><b className="p-eye l" /><b className="p-eye r" /></i><i className="p-hair" /></span></span><span>{role}</span></div>; }
export default function MissionExperience() {
  const [state, setState] = useState(initial);
  const [intro, setIntro] = useState(true);
  const [phase, setPhase] = useState(0);
  const [thought, setThought] = useState(false);
  const [hydrated, setHydrated] = useState(false);
  const bodyRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const startRef = useRef<HTMLButtonElement>(null);
  const stateRef = useRef(state);
  const scene = data.scenes[state.scene];
  const room = state.room || physicalRoom(scene.space);
  const inContext = room === physicalRoom(scene.space);
  const eligibleCases = data.cases.filter(c => c.steps.some(s => s.scene === scene.id));
  const selectedCase = eligibleCases.find(c => c.id === state.caseId);
  useEffect(() => {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch {}
    const next = restore(saved, location.search);
    stateRef.current = next;
    // eslint-disable-next-line react-hooks/set-state-in-effect -- restore browser-only navigation after hydration
    setState(next); setIntro(!next.started); setHydrated(true);
    const back = () => {
      const restored = restore(stateRef.current, location.search);
      stateRef.current = restored; setState(restored); setPhase(0); setThought(false);
      bodyRef.current?.scrollTo(0, 0);
    };
    window.addEventListener('popstate', back);
    return () => window.removeEventListener('popstate', back);
  }, []);
  function navigate(next: typeof state, replace = false) {
    stateRef.current = next; setState(next); if (next.scene !== state.scene) { setPhase(0); setThought(false); }
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); } catch {}
    const url = new URL(location.href);
    url.searchParams.set('mission', '1'); url.searchParams.set('scene', data.scenes[next.scene].id);
    if (next.caseId) url.searchParams.set('case', next.caseId); else url.searchParams.delete('case');
    history[replace ? 'replaceState' : 'pushState'](null, '', url);
    bodyRef.current?.scrollTo(0, 0);
    requestAnimationFrame(() => {
      titleRef.current?.focus({ preventScroll: true });
      if (next.caseId && next.scene === state.scene) {
        const target = bodyRef.current?.querySelector('.m1-case-trace');
        const panel = bodyRef.current;
        if (target && panel) panel.scrollTop += target.getBoundingClientRect().top - panel.getBoundingClientRect().top - 20;
      }
    });
  }
  function start() { setIntro(false); navigate({ ...state, started: true }); }
  const title = sceneTitles[scene.id] ?? scene.title;
  const maxPhase = ['M1-02', 'M1-12'].includes(scene.id) ? 2 : scene.id === 'M1-01' ? 1 : 0;
  const revealText = selectedCase?.steps.filter(s => s.scene <= scene.id).at(-1)?.copy ?? (scene.id === 'M1-12' ? `최초 ${data.capacity.initial}h → 수요 ${data.capacity.demand}h → 부족 ${data.capacity.gap}h. 추가 ${data.capacity.additional}h 확보 → 변경 후 ${data.capacity.revised}h.` : scene.id === 'M1-24' ? `실제 입사 ${data.outcomes.joined}명. 업무 준비 확인 ${data.outcomes.ready}명, 목표일까지 확인 ${data.outcomes.targetDateReady}명. 계획과 실제를 구분합니다.` : '저장된 근거와 사람의 판단을 순서대로 확인합니다. 새로운 AI 평가를 실행하지 않습니다.');
  return <main className="po-app m1-app" data-dataset-version={data.datasetVersion}>
    <div className="po-shell" inert={intro}>
      <header className="m1-header"><a className="po-brand" href="#office"><span>▦</span>PeopleOps Office</a><div><b>Mission 1 · 신입 ML Engineer</b><small>시나리오 가정 · 승인 Baseline v1</small></div><button ref={startRef} onClick={() => setIntro(true)}>Mission 안내</button></header>
      <nav className="m1-progress" aria-label="Mission 1 상위 진행도">{data.stages.map((stage, i) => {
        const first = data.scenes.findIndex(s => s.stage === i);
        const completed = state.done || i < data.scenes[state.frontier].stage;
        const current = state.started && scene.stage === i;
        const available = first <= state.frontier && state.started;
        return <button key={stage} disabled={!state.started || first > state.frontier} aria-current={current ? 'step' : undefined} data-stage={i} data-status={current ? 'CURRENT' : completed ? 'COMPLETED' : available ? 'AVAILABLE' : 'UPCOMING'} onClick={() => navigate(move(state, first))}><span>{i + 1}</span><b>{stage}</b><small>{current ? (state.done ? '완료 · 다시 보기' : '현재') : completed ? '완료' : available ? '진행 중' : '예정'}</small></button>;
      })}</nav>
      <div className="m1-workspace" id="office">
        <section className="win m1-panel" aria-label="판단 기록">
          <header className="win-bar"><span>판단 기록 · {state.started ? scene.id : 'Mission 안내'}</span><span>{scene.space}</span></header>
          <div className="m1-panel-body" ref={bodyRef}>
            <h1 ref={titleRef} tabIndex={-1}>{state.started ? copy(scene.question) : '인력 확보의 과정을 따라가 보세요.'}</h1>
            {!state.started ? <><p>인력 요청부터 근거 확인, 사람의 판단, 입사 후 업무 준비까지 탐색합니다.</p><button className="po-primary" onClick={start}>Mission 시작 →</button></> : <>
              <p className="m1-subtitle">{title}</p>
              {think[scene.id] && <aside className="m1-think"><b>잠깐 생각해 보기</b><p>{think[scene.id]}</p><p>{thought ? '아래에서 기록된 근거를 확인합니다.' : '생각한 뒤 아래 근거 확인 버튼으로 이어가세요.'}</p><small>정답·점수·결과 변경은 없습니다.</small></aside>}
              {(!think[scene.id] || thought) && <SceneContent id={scene.id} phase={phase} />}
              {eligibleCases.length > 0 && (!think[scene.id] || thought) && <section className="m1-case-questions" aria-label="판단 질문"><h3>사람의 판단을 따라가기</h3>{eligibleCases.map(c => <button key={c.id} aria-expanded={selectedCase?.id === c.id} onClick={() => navigate({ ...state, caseId: selectedCase?.id === c.id ? '' : c.id })}>{c.question}<span>{selectedCase?.id === c.id ? '접기 −' : '열기 →'}</span></button>)}</section>}
              {(phase >= maxPhase) && (!think[scene.id] || thought) && <StoredReveal key={`${scene.id}-${state.caseId}-${phase}`} text={copy(revealText)} />}
              {selectedCase && <RepresentativeCase item={selectedCase} scene={scene.id} />}
              <details className="m1-source"><summary>자료 출처와 확인 범위</summary><p>합성 Plan·기록: Dataset v1 / {data.sourcePath}. 대표 사례는 확정된 Presentation Mapping {data.mappingVersion}을 참조합니다.</p><p>공개 공고 전문과 Values 공식 원문은 미확보입니다. 기아 내부 데이터·공식 운영정책으로 해석하지 않습니다.</p></details>
              {state.done && scene.id === 'M1-25' && <p className="m1-message" role="status">Mission 1 탐색 완료 · 채용 성공 판정과는 다릅니다. Mission 2는 아직 시작하지 않았습니다.</p>}
            </>}
          </div>
          {state.started && <footer className="m1-controls"><button disabled={state.scene === 0} onClick={() => navigate(move(state, state.scene - 1))}>← 이전</button>{think[scene.id] && !thought ? <button className="po-primary" onClick={() => setThought(true)}>근거 확인 →</button> : phase < maxPhase ? <button className="po-primary" onClick={() => setPhase(p => p + 1)}>{scene.id === 'M1-01' ? '목표 브리핑 확인' : phase === 0 ? '계산 근거 확인' : '운영 판단과 대안 확인'} →</button> : <button className="po-primary" disabled={state.done && state.scene === 24} onClick={() => navigate(advance(state))}>{state.scene === 24 ? state.done ? '탐색 완료' : 'Mission 1 탐색 마치기' : state.scene === 5 ? 'HR 화면으로 복귀 →' : `다음 · ${sceneTitles[data.scenes[state.scene + 1].id] ?? data.scenes[state.scene + 1].title} →`}</button>}</footer>}
        </section>
        <aside className="m1-human-column">
          <section className={`win m1-office ${scene.space.includes('Mode') && state.started ? 'm1-special' : ''}`} aria-label="PeopleOps Office 공간 지도">
            <header className="win-bar"><span>업무 공간 · {room}</span><span>7개 공간</span></header>
            <div className="m1-rooms">{rooms.map((name, i) => <button key={name} data-room={name} aria-pressed={room === name} onClick={() => { setState(s => ({ ...s, room: name })); }} className={`m1-room ${room === name ? 'selected' : ''}`}><span>{name}</span><span className="m1-mini-room" aria-hidden="true"><i className="pr pr-desk"><i className="pr-monitor" /></i><i className="pr pr-shelf" /><i className="m1-room-dot" style={{ background: ['#b8f0dd', '#c9b8ff', '#fff3b0'][i % 3] }} /></span><small>{name === physicalRoom(scene.space) && state.started ? '현재 업무' : '공간 둘러보기'}</small></button>)}</div>
            <button className="m1-board-button" aria-label="Mission Board 열기" onClick={() => { if (state.started) navigate(move(state, 0)); else setIntro(true); }}>▤ Mission Board · 요청과 목표</button>
          </section>
          <section className="win m1-human" aria-label="사람과 업무"><header className="win-bar"><span>{state.started && inContext ? scene.space.replace(' Mode', '') : room}</span><span>사람의 업무</span></header><div className="m1-human-body">{state.started && inContext ? <><div className="m1-people">{scene.roles.map((role, i) => <PixelPerson key={role} role={copy(role)} index={i} />)}</div><h2>{title}</h2><p>{scene.id === 'M1-25' ? '다음 Mission에서 이전 데이터를 분석할 수 있도록 기준 Dataset을 확인합니다. 이번 탐색에서는 분석을 시작하지 않습니다.' : copy(scene.human)}</p><p className="m1-note">{scene.id === 'M1-25' ? '승인 Dataset v1 → 다음 분석에서 사용할 기준선' : scene.id === 'M1-12' ? '문제 발견 → 계산 확인 → 대안 검토 → 추가 시간 확보 → 일정 반영' : copy(scene.interaction)}</p><small>사전 구성된 합성 업무 맥락 · 실제 직원의 대화가 아닙니다.</small></> : <><p>이 공간을 둘러보고 있습니다. 아직 도달하지 않은 업무 결과는 공개하지 않습니다.</p>{state.started && <button onClick={() => setState(s => ({ ...s, room: '' }))}>현재 업무로 돌아가기</button>}</>}</div></section>
          <details className="m1-scene-list"><summary>진행한 Scene 다시 보기 · {state.started ? state.scene + 1 : 0} / {data.scenes.length}</summary><nav aria-label="Mission 1 Scene 선택">{data.scenes.map((s, i) => <button key={s.id} disabled={!state.started || i > state.frontier} aria-current={i === state.scene && state.started ? 'step' : undefined} onClick={() => navigate(move(state, i))}>{s.id} · {sceneTitles[s.id] ?? s.title}{i > state.frontier ? ' · 예정' : ''}</button>)}</nav><p>완료된 내용 재방문은 실제 진행 위치나 Dataset을 바꾸지 않습니다.</p>{state.scene < state.frontier && <button onClick={() => navigate(move(state, state.frontier))}>진행 중인 Scene으로 돌아가기</button>}</details>
          <p className="m1-note m1-mobile-note">좁은 화면에서는 판단 기록을 먼저 읽습니다. 공간 탐색은 데스크톱을 권장합니다.</p>
        </aside>
      </div>
      <footer className="po-footer">PeopleOps Office · 합성 HR 시나리오 · 데이터 기준 v1<br />원본 Pixel Office: 갓생맘 🎀 · <a href="https://www.instagram.com/godseng.mom/" target="_blank" rel="noreferrer">@godseng.mom</a><br />© godseng.mom · 자유롭게 쓰되 무단 재판매 금지</footer>
    </div>
    {intro && hydrated && <MissionIntro onStart={start} onClose={() => { setIntro(false); requestAnimationFrame(() => startRef.current?.focus()); }} />}
    {!hydrated && <dialog aria-labelledby="intro-title" className="m1-loading-intro"><h2 id="intro-title">Machine Learning Engineer · Mission 시작</h2></dialog>}
  </main>;
}
