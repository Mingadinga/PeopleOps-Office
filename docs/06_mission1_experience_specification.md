# PeopleOps Office — V2 Mission 1 Experience

## 1. 책임과 진행

본 문서는 확정 Mission 1 Journey를 Scene Contract로 문서화한다. 아래 M1-번호는 이 문서의 추적 ID이며
새로운 기능이나 결과를 추가한 것이 아니다. UI는 [05](05_ui_specification.md), 채용 판단은
[07](07_recruitment_design_specification.md), 필드/enum은 [09](09_mission1_data_specification.md)를 따른다.

상위 진행도는 인력계획 / 인재 정의 / 채용 설계 / 지원자 검증 / 인재 확보 / 업무 준비다.
완료 요약은 다시 볼 수 있고 예정 단계 Jump는 불가하다. Scene 이동은 명시적 진행 행동을 따른다.
Room은 장소이며 같은 공간에서 여러 Scene을 진행한다.

## 2. Scene Contract

모든 Scene에는 Core Question / Participants / Trigger / Human Layer / Interaction /
Decision Layer / Evidence / Decision / State Transition / Next Question의 10개 항목을 둔다.
장소는 맥락 속성으로 추가한다. 아래 계약의 Decision은 Case에 기록된 사람 판단 또는 그 탐색 목적이며
제품 사용자가 채용 결과를 새로 결정한다는 의미가 아니다.

공통 Trigger는 앞 Scene의 내용을 확인하고 다음 CTA를 누르는 행동이다. 첫 Scene은 Mission 시작이다.
상태 전이는 명시적 진행으로만 다음 Scene에 연결하며 시간 경과·카메라 완료·AI 결과로 자동 진행하지 않는다.
자료 미생성은 탐색 진행/채용 결과와 별개 상태다. 준비 상태를 0·합격·Ready로 채우지 않는다.
과거 예시 결과나 3명 Evidence Pattern을 실제 Dataset 결과로 미리 확정하지 않는다.
대표 3명은 Freeze 후 선정하며 Pattern은 Desired Contrast다. 별도 Presentation Mapping은 09를 따른다.

판단 계보는 `Raw Evidence → Human Observation → Skill Decision → Final Hiring Decision`이며 Stage Transition은 별도 운영 판단이다.
아래 Scene은 최신 계약의 경험 설계다. v0.1은 Audit 이력이고 새 Dataset·대표 3명은 미생성/미선정이다.

## 3. Mission 1 Scene 목록

### M1-01. 인력 요청

- **Stage / Space:** 인력계획 / Mission Board
- **Core Question:** 어떤 업무 인력이 언제 필요한가?
- **Participants:** 현업 채용책임자, ICT 인사담당자
- **Trigger:** Mission 시작 CTA
- **Human Layer:** 현업이 필요 인력과 목표일을 요청한다.
- **Interaction:** 요청서 확인 → Goal Briefing → 인력계획 시작
- **Decision Layer:** 직무, Demand 16 FTE, 목표 Ready 2027-09. Gap은 미공개.
- **Evidence:** 02의 합성 요청·Plan. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 요청을 검증할 인력계획 질문으로 연결한다.
- **State Transition:** 현재 내용 확인 후 M1-02. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 목표시점에 필요한 인력이 충분한가?

### M1-02. 인력계획

- **Stage / Space:** 인력계획 / 인력계획실
- **Core Question:** 목표시점에 필요한 인력이 충분한가?
- **Participants:** ICT 인사담당자, 현업 채용책임자
- **Trigger:** M1-01 확인 후 다음 CTA
- **Human Layer:** 현재 인력과 확정 이동을 확인하고 확보 대안을 논의한다.
- **Interaction:** 입력 확인 → Forecast 계산 → Gap 계산 → 근거·대안 확인
- **Decision Layer:** 12 + 1 - 1 + 0 = 12, 16 - 12 = 4 FTE. 멘토링·6개월 Ramp-up 조건.
- **Evidence:** 02 Plan(SYNTHETIC), 03 판단 근거(INFERENCE). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 조건을 검토한 결과 신입 외부채용을 기본 방향으로 정한다.
- **State Transition:** 현재 내용 확인 후 M1-03. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 어떤 기초와 성장 가능성이 필요한가?

### M1-03. 인재 요건 Workshop

- **Stage / Space:** 인재 정의 / 채용전략실
- **Core Question:** 어떤 기초와 성장 가능성이 필요한가?
- **Participants:** ICT 인사담당자, 현업 채용책임자, ML 엔지니어
- **Trigger:** M1-02 확인 후 다음 CTA
- **Human Layer:** 실제 업무를 설명하고 입사 전 필요 역량과 학습 가능 영역을 논의한다.
- **Interaction:** 업무 → Skill → 분류 → Evidence 펼치기
- **Decision Layer:** Must/Learnable/Plus와 기대 Evidence. 공개 요건과 해석 구분.
- **Evidence:** 02·07 직무 해석; KIA-02는 원문 미확보. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** V2 인재 요건을 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-04. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 업무와 요건을 어떻게 전달할 것인가?

### M1-04. 채용공고

- **Stage / Space:** 채용 설계 / 채용전략실
- **Core Question:** 업무와 요건을 어떻게 전달할 것인가?
- **Participants:** 채용담당자, ICT 인사담당자, ML 엔지니어
- **Trigger:** M1-03 확인 후 다음 CTA
- **Human Layer:** 요건을 공고 초안으로 옮긴다.
- **Interaction:** 초안과 인재 요건 연결 확인
- **Decision Layer:** 업무·Must/Plus·성장 정보의 연결
- **Evidence:** 07 설계(INFERENCE), 합성 공고 Case(SYNTHETIC). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 검토할 공고 초안을 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-05. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 공고에서 무엇을 더 명확히 해야 하는가?

### M1-05. 공고 점검

- **Stage / Space:** 채용 설계 / 채용전략실
- **Core Question:** 공고에서 무엇을 더 명확히 해야 하는가?
- **Participants:** 채용담당자, ICT 인사담당자
- **Trigger:** M1-04 확인 후 다음 CTA
- **Human Layer:** 시스템이 검토 지점을 표시하고 담당자가 문구를 확인한다.
- **Interaction:** 문장 → 점검 이유 → 수정 제안 → 사람의 확인
- **Decision Layer:** 모호한 표현·내부용어·요건 혼재. 자동 확정 없음.
- **Evidence:** 08 규칙, 합성 초안·검토 기록. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 사람이 확인한 공고 문구를 기록한다.
- **State Transition:** 현재 내용 확인 후 M1-06. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 공고와 전형 정보가 지원자에게 어떻게 보이는가?

### M1-06. 지원자 화면

- **Stage / Space:** 채용 설계 / 지원자 화면 Mode
- **Core Question:** 공고와 전형 정보가 지원자에게 어떻게 보이는가?
- **Participants:** 지원자
- **Trigger:** M1-05 확인 후 다음 CTA
- **Human Layer:** 지원자가 공고·질문·전형 안내를 탐색한다.
- **Interaction:** 지원자 화면 보기 → 안내 확인 → HR 화면 복귀
- **Decision Layer:** 공개정보와 합성 시나리오 안내의 경계
- **Evidence:** KIA-01 캡처(메타데이터 TO VERIFY), 합성 안내. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 지원 접점의 정보 전달을 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-07. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 어떤 인재에게 무엇을 어떻게 알릴 것인가?

### M1-07. 인재 유치

- **Stage / Space:** 채용 설계 / 채용전략실
- **Core Question:** 어떤 인재에게 무엇을 어떻게 알릴 것인가?
- **Participants:** ICT 인사담당자, 채용담당자
- **Trigger:** M1-06 확인 후 다음 CTA
- **Human Layer:** Target·Message·Content·Channel을 검토한다.
- **Interaction:** 대상 → 메시지 → 채널 근거 탐색
- **Decision Layer:** 직무 이해와 관심을 만드는 이유·계획 가정
- **Evidence:** 07 전략(INFERENCE/SYNTHETIC). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 인재 유치 전략의 근거를 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-08. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 질문에서 어떤 경험을 발견하고 후속 검증할 것인가?

### M1-08. 지원 질문 설계

- **Stage / Space:** 채용 설계 / 채용전략실
- **Core Question:** 질문에서 어떤 경험을 발견하고 후속 검증할 것인가?
- **Participants:** ICT 인사담당자, 채용담당자
- **Trigger:** M1-07 확인 후 다음 CTA
- **Human Layer:** 제공된 3문항의 의도와 한계를 논의한다.
- **Interaction:** 문항 → Evidence 목적 → 후속 검증
- **Decision Layer:** 성장, 중요 역량·노력, 가치·행동. 글만으로 역량 확정 금지.
- **Evidence:** KIA-01 내용 캡처, 07 해석. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 질문을 경험 탐색의 출발점으로 사용한다.
- **State Transition:** 현재 내용 확인 후 M1-09. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 목표와 가용시간 안에서 어떤 운영 규모를 계획할 것인가?

### M1-09. Funnel Planning

- **Stage / Space:** 채용 설계 / 채용전략실
- **Core Question:** 목표와 가용시간 안에서 어떤 운영 규모를 계획할 것인가?
- **Participants:** ICT 인사담당자, 채용담당자, ML 엔지니어
- **Trigger:** M1-08 확인 후 다음 CTA
- **Human Layer:** HR이 목표를 제시하고 현업이 Capacity를 설명한다. 계산 후 Trade-off를 논의한다.
- **Interaction:** 목표 → 예상 전환 → 비용 → 60 person-hours → 계산 → 근거
- **Decision Layer:** cycle-level INITIAL_PLAN 60h, 후보당 면접 계획 3h, planned operational capacity 20명. quota 아님.
- **Evidence:** 07 Funnel/Capacity Plan(SYNTHETIC), 산술 근거. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 사람이 Capacity Plan을 검토한다. quota가 아니다.
- **State Transition:** 현재 내용 확인 후 M1-10. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 기본요건과 후속 검증할 경험은 무엇인가?

### M1-10. 서류

- **Stage / Space:** 지원자 검증 / 채용운영실
- **Core Question:** 기본요건과 후속 검증할 경험은 무엇인가?
- **Participants:** 채용담당자, ICT 인사담당자
- **Trigger:** M1-09 확인 후 다음 CTA
- **Human Layer:** 지원정보와 SELF_REPORTED 원답변에서 기본요건, Evidence Candidate, 후속검증 질문을 찾는다.
- **Interaction:** 답변 → 요건/경험 → 후속 확인점
- **Decision Layer:** 원본 답변과 기록된 서류 판단·불확실성
- **Evidence:** applications, assessment_evidence, stage_history의 합성 기록. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** DOCUMENT_SCREEN Stage Transition과 후속 확인점을 탐색한다. Skill 확정이나 최종 합격 판단이 아니다. 새 계약 결과는 미생성.
- **State Transition:** 현재 내용 확인 후 M1-11. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 면접 전에 어떤 기본기를 확인하는가?

### M1-11. 사전검증

- **Stage / Space:** 지원자 검증 / 온라인 평가 화면 Mode
- **Core Question:** 면접 전에 어떤 기본기를 확인하는가?
- **Participants:** 지원자
- **Trigger:** M1-10 확인 후 다음 CTA
- **Human Layer:** 지원자가 역량검사·코딩테스트를 수행하는 맥락을 본다.
- **Interaction:** 단계 안내 → 코딩 기본기 근거 → 기록 확인
- **Decision Layer:** PRE_ASSESSMENT의 APTITUDE/CODING_TEST Activity. 역량검사는 이벤트만, 코딩은 구현·검증 기본기
- **Evidence:** 07 시나리오, stage_history·assessment_activities·코딩 Evidence. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 직접 Task의 기초 Evidence와 Stage 진행 판단을 확인한다. 미확인을 Skill 부족으로 변환하지 않는다. 실제 기업 문항 재현 없음.
- **State Transition:** 현재 내용 확인 후 M1-12. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 실제 면접 필요 인원을 현재 평가자 Capacity로 운영할 수 있는가?

### M1-12. 1차면접 Capacity 재검토

- **Stage / Space:** 지원자 검증 / 평가회의실
- **Core Question:** 실제 면접 필요 인원을 현재 평가자 Capacity로 운영할 수 있는가?
- **Participants:** ICT 인사담당자, 채용담당자, ML 엔지니어, 현업 채용책임자
- **Trigger:** M1-11 확인 후 다음 CTA
- **Human Layer:** 초기 계획 3h × 20명 = 60h와 실제 사전검증 후 평가 수요를 비교한다. 시스템은 Gap을 계산하고 HR은 추가 자원/기간 조정/평가방식 재설계 중 운영 대응을 설명한다.
- **Interaction:** Initial Plan → Demand → Gap → 대안 → Human Decision → Revised Capacity
- **Decision Layer:** 추가 Resource 확보 / 기간 조정 / 평가방식 재설계
- **Evidence:** v0.2 검토 후보의 Funnel Actual, interview_capacity_events, capacity_assignments와 Participant 근거. 09 §3.2/4.17 Decision Note의 192×4=768h 수요 → Gap 688h → 80h panel 9개 추가 → Revised 800h를 추적한다. 미승인·미Freeze 상태이며 UI 연결 완료를 뜻하지 않는다.
- **Decision:** 추가 평가자 Resource 확보를 선택한 SYNTHETIC_HUMAN_SCENARIO 운영 판단과 대안을 추적한다. 800h는 목표 Join을 맞춘 역산값이나 시스템의 최적 추천이 아니다. Capacity 부족으로 후보자를 탈락시키지 않으며 Initial Plan → Gap → Human Decision → Revised → Actual Consumption 이력과 reusable pool의 예약·해제를 보존한다.
- **State Transition:** 현재 내용 확인 후 M1-13. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 확보한 Capacity 안에서 각 역량을 어떤 방식으로 검증할 것인가?

v0.3부터 M1-12는 09의 60h 계획·고정 evaluator pool 추가시간 계약을 따른다. 위 800h는 v0.2 이력 비교다.

### M1-13. 1차면접 설계

- **Stage / Space:** 지원자 검증 / 평가회의실
- **Core Question:** 각 역량을 어떤 방식으로 검증할 것인가?
- **Participants:** ML 엔지니어, 현업 채용책임자, ICT 인사담당자
- **Trigger:** M1-12 확인 후 다음 CTA
- **Human Layer:** 주 평가와 보완 검증을 논의한다.
- **Interaction:** Skill → Matrix → 평가 이유
- **Decision Layer:** 기술평가·AI 과제·질의의 역할과 중복 방지
- **Evidence:** 07 Assessment Matrix(INFERENCE/SYNTHETIC). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 1차면접의 구조화된 검증 방식을 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-14. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 답변과 과제에서 무엇이 확인되고 무엇이 남는가?

### M1-14. 1차 실무진면접

- **Stage / Space:** 지원자 검증 / 면접실
- **Core Question:** 답변과 과제에서 무엇이 확인되고 무엇이 남는가?
- **Participants:** 지원자, ML 엔지니어, 현업 채용책임자
- **Trigger:** M1-13 확인 후 다음 CTA
- **Human Layer:** 평가자 3명의 단일 60분 Session 안에서 기술평가·AI 과제·질의 Evidence를 본다. 세 영역 시간을 중복 합산하지 않는다.
- **Interaction:** 대표 3명 답변·원근거·Skill 연결·사람의 수준 확인
- **Decision Layer:** 원답변/과제, AI 후보와 사람의 연결, Evidence Level, 불확실성
- **Evidence:** 원본·Skill Link·Observation 합성 기록과 Freeze 후 대표 Mapping(09). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 확인된 Evidence를 기록하며 합불을 선결정하지 않는다.
- **State Transition:** 현재 내용 확인 후 M1-15. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 평가자 차이를 어떤 원근거로 검토하는가?

### M1-15. 1차 평가 조정

- **Stage / Space:** 지원자 검증 / 평가회의실
- **Core Question:** 평가자 차이를 어떤 원근거로 검토하는가?
- **Participants:** ML 엔지니어, 현업 채용책임자, ICT 인사담당자
- **Trigger:** M1-14 확인 후 다음 CTA
- **Human Layer:** 평가자가 저장된 Observation의 부족·한계·이견을 확인하고 필요한 경우에만 별도 Calibration을 수행한다. 핵심 Skill01~03의 decisionable Coverage와 역량 충분성을 구분한다. 직접 LIMITED도 관찰 Coverage에 포함하며 명시적 비진행 판단은 별도다. 합의된 LIMITED/NOT_OBSERVED만으로 Calibration을 만들지 않는다.
- **Interaction:** 차이 → 원문 → Rubric → 재검토
- **Decision Layer:** AGREED / DISAGREEMENT_REMAINS / INSUFFICIENT_EVIDENCE
- **Evidence:** assessment_observations, evidence_decisions, skill_decision_observations. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** Evidence Evolution / Context Difference / Evaluator Disagreement를 구분하여 합의·미합의·근거 부족을 보존한다. Observation을 우회하거나 최신 Evidence를 자동 우선하지 않는다.
- **State Transition:** 현재 내용 확인 후 M1-16. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 실제 협업·학습·가치와 행동은 어떻게 확인되는가?

### M1-16. 2차면접

- **Stage / Space:** 지원자 검증 / 면접실
- **Core Question:** 실제 협업·학습·가치와 행동은 어떻게 확인되는가?
- **Participants:** 지원자, 면접관
- **Trigger:** M1-15 확인 후 다음 CTA
- **Human Layer:** 평가자 2명·30분의 합성 면접에서 구체적 과거 행동과 후속 질문을 탐색한다. 기아 공식 운영정책이 아니다.
- **Interaction:** 질문 → 답변 → 행동 근거 → 관찰
- **Decision Layer:** 기술평가 반복이나 Culture Fit 점수 없이 행동 확인
- **Evidence:** 07 시나리오·관찰; KIA-04 SOURCE NOT AVAILABLE. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 업무 방식의 Evidence와 확인 한계를 기록한다.
- **State Transition:** 현재 내용 확인 후 M1-17. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 필수 근거와 남은 불확실성에 비추어 어떻게 판단했는가?

### M1-17. 최종검토

- **Stage / Space:** 인재 확보 / 평가회의실
- **Core Question:** 필수 근거와 남은 불확실성에 비추어 어떻게 판단했는가?
- **Participants:** ICT 인사담당자, 현업 채용책임자
- **Trigger:** M1-16 확인 후 다음 CTA
- **Human Layer:** 저장된 Skill Decision·Observation 계보와 Learnable Gap·평가 조정을 검토한다.
- **Interaction:** Must → 불확실성 → Gap → 조정 → 기록된 판단
- **Decision Layer:** 총점·순위 없이 Coverage와 rationale
- **Evidence:** final_decisions와 근거 참조. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** INITIAL의 PROCEED_TO_OFFER / DO_NOT_PROCEED / HOLD를 추적한다. HOLD는 Reason+Resolution Plan이 필수이며 terminal outcome이 아니다. 값은 미생성.
- **State Transition:** 현재 내용 확인 후 M1-18. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** HOLD의 어떤 질문을 추가로 확인해야 하는가?

### M1-18. HOLD Focused Follow-up

- **Stage / Space:** 인재 확보 / 면접실
- **Core Question:** HOLD의 어떤 질문을 추가로 확인해야 하는가?
- **Participants:** 지원자, 해당 Skill 평가자, ICT 인사담당자
- **Trigger:** M1-17 확인 후 다음 CTA
- **Human Layer:** INITIAL HOLD의 Reason·Resolution Plan·기존 Evidence/Observation·미해결 질문에 직접 대응하는 확인을 수행한다. 일반 패턴 재추출을 통한 추가 합격 기회로 만들지 않는다.
- **Interaction:** Reason + Plan → 최대 1회 Focused Follow-up → new Evidence → new Observation
- **Decision Layer:** 전체 면접 반복·rescue·결과 강제 금지
- **Evidence:** final_decisions, FOCUSED_FOLLOW_UP Activity, 새 assessment_evidence/assessment_observations
- **Decision:** 새 관찰을 별도 저장한다. 기존 근거를 덮어쓰지 않는다. HOLD가 없는 경우 미해당 요약만 표시한다.
- **State Transition:** 현재 내용 확인 후 M1-19. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 새 관찰로 불확실성과 평가자 차이가 해소됐는가?

### M1-19. Calibration과 Final Re-review

v0.4: MUST 자체가 판단 불가능하면 Offer 진행하지 않는다. 최대 1회 후 미확보는 판단 근거 부족으로 DO_NOT_PROCEED 종료하며 역량 부족으로 단정하지 않는다. 비핵심 Context/Learnable 불확실성만 rationale과 함께 수용할 수 있다.

- **Stage / Space:** 인재 확보 / 평가회의실
- **Core Question:** 후속 관찰을 포함해 최종 채용 판단을 내릴 수 있는가?
- **Participants:** 해당 Skill 평가자, 현업 채용책임자, ICT 인사담당자
- **Trigger:** M1-18 확인 후 다음 CTA
- **Human Layer:** persisted Observation 기반 Calibration 뒤 남은 uncertainty를 검토한다.
- **Interaction:** 새 Observation → Calibration → RE_REVIEW
- **Decision Layer:** Evolution/Context Difference/Disagreement 구분, RE_REVIEW의 HOLD 금지
- **Evidence:** skill_decision_observations, evidence_decisions, final_decisions의 review_round
- **Decision:** INITIAL HOLD에 대해 PROCEED_TO_OFFER 또는 DO_NOT_PROCEED를 기록한다. 미완료는 미완료로 보존하며 결과를 강제하지 않는다.
- **State Transition:** 현재 내용 확인 후 M1-20. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 제안 이후 응답과 입사 변동은 무엇인가?

### M1-20. Offer

- **Stage / Space:** 인재 확보 / 채용운영실
- **Core Question:** 제안 이후 응답과 입사 변동은 무엇인가?
- **Participants:** 채용담당자, ICT 인사담당자
- **Trigger:** M1-19 확인 후 다음 CTA
- **Human Layer:** 기록된 Offer·응답·확인된 사유를 확인한다.
- **Interaction:** 제안 → 응답 → 상태/사유
- **Decision Layer:** response_deadline·관측창·Response Event로 Open/EXPIRED를 구분. 수락·거절·입사 전 철회와 UNKNOWN 보존
- **Evidence:** offers, offer_events. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** PROCEED_TO_OFFER만 제안으로 연결한다. EXPIRED는 deadline까지 응답 부재에서 파생하며 NO_RESPONSE의 motive를 추론하지 않는다. Offer와 Join을 구분한다.
- **State Transition:** 현재 내용 확인 후 M1-21. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 입사를 실제 가용 인력으로 바로 볼 수 있는가?

### M1-21. Join

- **Stage / Space:** 인재 확보 / 업무공간
- **Core Question:** 입사를 실제 가용 인력으로 바로 볼 수 있는가?
- **Participants:** 신규 입사자, ICT 인사담당자
- **Trigger:** M1-20 확인 후 다음 CTA
- **Human Layer:** 입사 확인 후 업무 준비 과정을 안내한다.
- **Interaction:** 입사 기록 → 목표시점 공급의 의미
- **Decision Layer:** JOINED ≠ READY
- **Evidence:** offers, onboarding_profiles, workforce_events. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 온보딩과 Ready 확인으로 연결한다.
- **State Transition:** 현재 내용 확인 후 M1-22. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 어떤 Gap을 어떤 업무로 줄일 것인가?

### M1-22. Onboarding

- **Stage / Space:** 업무 준비 / 업무공간
- **Core Question:** 어떤 Gap을 어떤 업무로 줄일 것인가?
- **Participants:** 신규 입사자, 온보딩 멘토, ICT 인사담당자
- **Trigger:** M1-21 확인 후 다음 CTA
- **Human Layer:** 개인별 learnable_gap_summary와 입사 후 관찰로 Gap·Ramp-up을 협의한다. 모든 Joiner에게 동일 Gap을 강제하지 않는다.
- **Interaction:** Gap → 1/3/6개월 Task → 실제 업무 근거
- **Decision Layer:** 초기 Evidence 재확인, 목적에 필요한 정보만 전달
- **Evidence:** onboarding_profiles/skill_gaps/tasks. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 사람이 기록한 Ramp-up 계획과 진행을 확인한다.
- **State Transition:** 현재 내용 확인 후 M1-23. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 실제 업무를 수행할 준비가 되었는가?

### M1-23. Ready

- **Stage / Space:** 업무 준비 / 업무공간
- **Core Question:** 실제 업무를 수행할 준비가 되었는가?
- **Participants:** 신규 입사자, 온보딩 멘토
- **Trigger:** M1-22 확인 후 다음 CTA
- **Human Layer:** planned_ready_at과 실제 post-join Work Evidence, 멘토/현업의 확인 주체·시각을 본다.
- **Interaction:** Task·개인별 Gap·업무 근거 → Human Confirmation → READY_CONFIRMED/연장 기록
- **Decision Layer:** ONBOARDING / READY / RAMP_UP_EXTENDED
- **Evidence:** onboarding_tasks, workforce_events. 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 사람의 Ready 확인과 effective_at을 공급 계산에 연결한다. 결과는 미확정.
- **State Transition:** 현재 내용 확인 후 M1-24. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 목표와 실제 결과는 어떻게 다른가?

### M1-24. Mission 1 결과

- **Stage / Space:** 업무 준비 / Mission Board
- **Core Question:** 목표와 실제 결과는 어떻게 다른가?
- **Participants:** ICT 인사담당자, 현업 채용책임자
- **Trigger:** M1-23 확인 후 다음 CTA
- **Human Layer:** 초기 인력계획과 실제 결과를 세 영역으로 확인한다.
- **Interaction:** Target/Actual/근거 → 데이터 분석 시작
- **Decision Layer:** Workforce / Recruiting Process / Onboarding의 WHAT
- **Evidence:** Plan + 실제 코드의 Analysis JSON(미생성). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 실제 결과를 확인하고 분석 질문으로 연결한다. WHY는 아직 단정하지 않는다.
- **State Transition:** 현재 내용 확인 후 M1-25. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 이 데이터를 새로운 경력채용 계획에 어떻게 활용할 것인가?

### M1-25. Data Lab 연결

- **Stage / Space:** Mission 전환 / 데이터랩
- **Core Question:** 이 데이터를 새로운 경력채용 계획에 어떻게 활용할 것인가?
- **Participants:** ICT 인사담당자, 인사 데이터 분석가
- **Trigger:** M1-24 확인 후 다음 CTA
- **Human Layer:** 새 요청의 조건과 분석할 이전 데이터를 연결한다.
- **Interaction:** Mission 2 문맥 → 새 요청 확인
- **Decision Layer:** 이전 Dataset과 새 모집단 조건의 구분
- **Evidence:** Mission 1 manifest, Mission 2 시나리오(수치 미정). 생성·검증 여부와 Provenance를 구분한다.
- **Decision:** 10의 새 경력 요청·Capability Gap·분석으로 이어진다.
- **State Transition:** 현재 내용 확인 후 Mission 2 M2-01. 상위 Stage가 바뀌면 이전 Stage를 탐색 완료로 기록한다.
- **Next Question:** 이번에는 어떤 Capability가 언제 필요한가?

HOLD subflow는 M1-18~19이며 모든 사용자는 같은 Case 흐름을 탐색한다. 후보자의 기록이 INITIAL HOLD일 때만
후속검증/재검토 이력을 보여주고, 미해당/미완료는 그대로 표시한다. 탐색 완료가 채용 상태 완료를 뜻하지 않는다.
Offer/Join 기록이 없는 후보자는 해당 결과를 만들지 않는다. 사용자 클릭으로 결과가 바뀌는 분기가 아니다.
M1-12의 Capacity 재검토와 M1-18~19 추가에 따라 Scene은 M1-01~25로 재정렬했다.

## 4. 공통 경험 규칙

기본은 Guided Exploration이다. Think Before Reveal은 Mission 1에서 약 5~7회 수준이며
인력계획 기준시점, 주 평가 방식, 근거 부족, 평가자 차이, Join/Ready 등 판단 원리를 생각하는 데 사용한다.
정확한 배치·문구는 후속 표현 조정이며 정답 점수·사람 순위·결과 분기를 추가하지 않는다.

캐릭터는 정보 제공·판단·논의·지원·영향 관계가 필요할 때만 등장한다.
사람 대화는 Typing 없이 표시하고 시스템 계산·검색만 Skip 가능한 Reveal로 보여준다.
Human Layer에서 업무가 발생하고 Decision Layer에 확인한 근거와 판단이 남는다.
같은 자료를 다시 볼 수 있으며 원문·상세 열기는 결과를 바꾸지 않는다.

Mission 1 결과는 세 Outcome의 WHAT까지만 다룬다. WHY·가설·추가 분석은 Mission 2에서 진행한다.
KPI는 마지막에 임의로 추가하는 수치가 아니라 Plan과 Stage/Offer/Ready Event에서 추적한다.
대표 사례의 Freeze 후 선정·Mapping은 09에 확정했다. 상세 배치·대사·복원(OPEN-13),
출처 부족(OPEN-10)은 [11](11_v2_migration_specification.md#7-open-issues)에 남긴다.
