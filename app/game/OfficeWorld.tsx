"use client";

import { useEffect, useRef, type CSSProperties } from "react";
import { nextStepId, rooms, stepStatus, type Destination, type NavigationState } from "../exploration/model";

const WIDTH = 960;
const HEIGHT = 650;
type Camera = { x: number; y: number; scale: number };

function PixelGuide({ color }: { color: string }) {
  return <span className="ag f-down a-idle po-guide" aria-hidden="true" style={{ "--hair": "#563d50", "--shirt": color, "--skin": "#ffdcc4" } as CSSProperties}>
    <span className="ag-body"><i className="p-shadow" /><i className="p-leg l" /><i className="p-leg r" /><i className="p-torso" /><i className="p-arm l" /><i className="p-arm r" /><i className="p-head"><b className="p-eye l" /><b className="p-eye r" /></i><i className="p-hair" /></span>
  </span>;
}

function RoomFurniture({ color }: { color: string }) {
  return <span className="po-furniture" aria-hidden="true">
    <span className="pr pr-shelf" style={{ left: 18, top: 32, width: 62, height: 16 }} />
    <span className="pr pr-desk" style={{ left: 84, top: 91, width: 82, height: 22 }}><i className="pr-monitor" /></span>
    <span className="pr pr-rug" style={{ left: 63, top: 138, width: 120, height: 37 }} />
    <PixelGuide color={color} />
    <span className="rm-door" style={{ left: 116, bottom: -3, width: 36 }} />
  </span>;
}

export default function OfficeWorld({ state, onSelect }: { state: NavigationState; onSelect: (id: Destination) => void }) {
  const viewportRef = useRef<HTMLDivElement>(null);
  const stageRef = useRef<HTMLDivElement>(null);
  const cameraRef = useRef<Camera>({ x: WIDTH / 2, y: HEIGHT / 2, scale: 0.6 });
  const targetRef = useRef<Camera>({ x: WIDTH / 2, y: HEIGHT / 2, scale: 0.6 });
  const modeRef = useRef<"fit" | "focus">("fit");
  const destinationRef = useRef(state.destination);
  const reducedRef = useRef(false);
  const dragRef = useRef({ active: false, moved: false, x: 0, y: 0, startX: 0, startY: 0 });
  const guidanceRef = useRef<() => void>(() => {});

  // The renderer retains the template's DOM camera/zoom/drag approach, without an engine tick.
  useEffect(() => {
    const viewport = viewportRef.current;
    const stage = stageRef.current;
    if (!viewport || !stage) return;
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const motionChanged = () => { reducedRef.current = media.matches; };
    motionChanged();
    media.addEventListener("change", motionChanged);
    const fitScale = () => Math.min(viewport.clientWidth / WIDTH, viewport.clientHeight / HEIGHT) * 0.94;
    const retarget = () => {
      const room = rooms.find(item => item.id === destinationRef.current);
      const scale = fitScale();
      const focusScale = Math.min(scale * 1.4, 1.35);
      const halfWidth = viewport.clientWidth / (2 * focusScale);
      const halfHeight = viewport.clientHeight / (2 * focusScale);
      const bound = (value: number, half: number, size: number) => half * 2 >= size ? size / 2 : Math.max(half, Math.min(size - half, value));
      targetRef.current = modeRef.current === "fit"
        ? { x: WIDTH / 2, y: HEIGHT / 2, scale }
        : { x: bound(room ? room.x + 132 : WIDTH / 2, halfWidth, WIDTH), y: bound(room ? room.y + 107 : HEIGHT / 2, halfHeight, HEIGHT), scale: focusScale };
    };
    guidanceRef.current = retarget;
    retarget();
    cameraRef.current = { ...targetRef.current };
    const observer = new ResizeObserver(retarget);
    observer.observe(viewport);
    let frame = 0;
    const paint = () => {
      const camera = cameraRef.current;
      const target = targetRef.current;
      const amount = reducedRef.current ? 1 : 0.12;
      camera.x += (target.x - camera.x) * amount;
      camera.y += (target.y - camera.y) * amount;
      camera.scale += (target.scale - camera.scale) * amount;
      stage.style.transform = `translate3d(${viewport.clientWidth / 2 - camera.x * camera.scale}px, ${viewport.clientHeight / 2 - camera.y * camera.scale}px, 0) scale(${camera.scale})`;
      frame = requestAnimationFrame(paint);
    };
    frame = requestAnimationFrame(paint);
    return () => { cancelAnimationFrame(frame); observer.disconnect(); media.removeEventListener("change", motionChanged); };
  }, []);

  useEffect(() => {
    destinationRef.current = state.destination;
    modeRef.current = state.started && state.destination !== "board" ? "focus" : "fit";
    guidanceRef.current();
  }, [state.destination, state.started, state.cameraRevision]);

  function select(id: Destination, keyboard: boolean) {
    if (keyboard || !dragRef.current.moved) onSelect(id);
  }

  return <section className="world-frame po-world" aria-label="PeopleOps Office 공간 지도">
    <div ref={viewportRef} className="world-viewport"
      onPointerDown={event => {
        if (event.button !== 0 || (event.target as HTMLElement).closest(".world-hud")) return;
        dragRef.current = { active: true, moved: false, x: event.clientX, y: event.clientY, startX: event.clientX, startY: event.clientY };
      }}
      onPointerMove={event => {
        const drag = dragRef.current;
        if (!drag.active) return;
        if (Math.hypot(event.clientX - drag.startX, event.clientY - drag.startY) > 5) drag.moved = true;
        if (drag.moved) {
          const scale = cameraRef.current.scale || 1;
          targetRef.current = { ...cameraRef.current,
            x: Math.max(0, Math.min(WIDTH, cameraRef.current.x - (event.clientX - drag.x) / scale)),
            y: Math.max(0, Math.min(HEIGHT, cameraRef.current.y - (event.clientY - drag.y) / scale)) };
          cameraRef.current = { ...targetRef.current };
        }
        drag.x = event.clientX; drag.y = event.clientY;
      }}
      onPointerUp={() => { dragRef.current.active = false; }}
      onPointerCancel={() => { dragRef.current.active = false; }}
      onPointerLeave={() => { dragRef.current.active = false; }}>
      <div ref={stageRef} className="world-stage" style={{ width: WIDTH, height: HEIGHT }}>
        <div className="world-floor" />
        <div className="po-corridor" aria-hidden="true">문제 → 근거 → 판단 → 다음 질문</div>
        {rooms.map((room, index) => {
          const status = room.id === "lab" ? state.destination === "lab" ? "CURRENT" : "UPCOMING" : stepStatus(room.id, state);
          const isNext = room.id === nextStepId(state);
          const label = status === "CURRENT" ? "현재 단계" : isNext ? "다음" : status === "REVIEWED" ? "✓ 확인함" : "살펴볼 단계";
          return <button key={room.id} className={`rm po-room ${status.toLowerCase()}${isNext ? " next" : ""}${state.briefing === "goal" && room.id !== "lab" ? " briefing-cue" : ""}`} data-room={room.id} data-status={status} data-next={isNext || undefined}
            aria-label={`${room.name} — ${room.question} — ${label}`}
            aria-current={status === "CURRENT" ? "step" : undefined}
            style={{ left: room.x, top: room.y, width: 264, height: 218, "--briefing-order": index } as CSSProperties}
            onClick={event => select(room.id, event.detail === 0)}>
            <span className="po-room-title"><span aria-hidden="true">{room.icon}</span> {room.name}</span>
            {(status !== "UPCOMING" || isNext) && <span className="po-room-status">{label}{status === "CURRENT" && state.reviewed.includes(room.id) ? " · ✓ 확인함" : isNext && state.reviewed.includes(room.id) ? " · ✓ 확인함" : ""}</span>}
            <RoomFurniture color={["#b8f0dd", "#c9b8ff", "#fff3b0", "#c9b8ff", "#ffb9d9", "#b8f0dd"][index]} />
            <span className="po-room-role">{room.role}{room.id === "lab" ? " · Mission 02" : ""}</span>
            <span className="po-room-question">{room.question}<b>살펴보기 →</b></span>
            {state.guidance && room.id === "workforce" && <span className="po-guidance">여기서 시작하세요</span>}
          </button>;
        })}
        <button className={`po-mission-board ${state.destination === "board" || state.destination === "kpi" ? "selected" : ""}${state.briefing === "goal" ? " briefing-cue" : ""}`}
          style={{ "--briefing-order": 5 } as CSSProperties}
          onClick={event => select("board", event.detail === 0)} aria-label="Mission Board 열기">
          <span aria-hidden="true">▤</span> Mission Board <small>채용 → 데이터 → 분석 → 개선</small>
        </button>
      </div>
      <div className="world-hud">
        <button onClick={() => { modeRef.current = "fit"; guidanceRef.current(); }}>전체 보기</button>
        <button onClick={() => { modeRef.current = "focus"; guidanceRef.current(); }}>선택 공간 보기</button>
      </div>
      <div className="world-hint">방을 눌러 살펴보기 · 드래그로 이동</div>
    </div>
  </section>;
}
