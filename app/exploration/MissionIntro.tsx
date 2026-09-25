"use client";

import { useEffect, useRef } from "react";

export default function MissionIntro({ onStart, onClose }: { onStart: () => void; onClose: () => void }) {
  const dialogRef = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const dialog = dialogRef.current;
    const previous = document.activeElement as HTMLElement | null;
    dialog?.showModal();
    return () => { dialog?.close(); if (previous?.isConnected) previous.focus(); };
  }, []);
  return <dialog ref={dialogRef} className="po-intro" aria-labelledby="intro-title" aria-describedby="intro-description" onCancel={event => { event.preventDefault(); onClose(); }}><div className="po-intro-card">
    <p className="po-kicker">PEOPLEOPS OFFICE · MISSION 01</p>
    <span className="po-intro-icon" aria-hidden="true">▦</span>
    <h1 id="intro-title">Machine Learning Engineer<br /><em>인력 확보</em></h1>
    <p id="intro-description">목표 시점에 필요한 인력을 확인하고<br />필요한 인재를 확보하는 과정을 탐색합니다.</p>
    <p className="po-intro-note">가상 인력 시나리오를 따라 데이터와 판단 근거를 살펴보세요.</p>
    <button className="po-primary po-intro-cta" onClick={onStart} autoFocus>Mission 시작 →</button>
    <button className="po-text-button" onClick={onClose}>먼저 Office 둘러보기</button>
  </div></dialog>;
}
