# PeopleOps Office — V2 UI / UX / Interaction Specification

## 1. 책임과 제품 경험

본 문서는 V2 UI/UX/Interaction의 최종 SSOT다. HR 정책은 [07](07_recruitment_design_specification.md),
AI 권한은 [08](08_hr_tech_specification.md), 데이터 계약은 [09](09_mission1_data_specification.md),
분석은 [10](10_mission2_analytics_specification.md)을 참조하며 다시 정의하지 않는다.
2026-09-24 동기화한 목표 설계이며 구현 완료 상태가 아니다. 현 구현은 [11](11_v2_migration_specification.md)에 기록한다.

PeopleOps Office는 ICT 인사담당자의 관점에서 하나의 채용 프로젝트가 사람의 업무·대화·근거·판단으로
진행되는 과정을 탐색하는 서비스다. Observe → Explore → Understand → Continue.
**People make decisions. Technology organizes evidence.**
로그인 없이 공개 URL로 접근하며 핵심 Mission은 외부 AI API 없이 동작한다.

## 2. Global Layout

Desktop First. 상단에 Mission 문맥과 6단계 진행도, 왼쪽에 Decision Layer, 오른쪽에 Human Layer,
하단에 Scene Control을 둔다. 한 순간의 Primary CTA는 하나다.

| 영역 | 보여주는 내용 |
|---|---|
| Human Layer | 누가 어디에서 어떤 업무·대화·회의·지원·시스템 처리를 하는가 |
| Decision Layer | 현재 질문, 확인한 데이터, Evidence, 검토 중인 가정, 판단 과정, 결정, 다음 질문 |
| Scene Control | 현재 공개 단계에 맞는 근거 확인·다음 진행·복귀 |

Human Layer의 변화와 왼쪽 기록은 같은 Scene을 참조한다. 도달하지 않은 결정은 먼저 표시하지 않는다.
Case Panel shell과 Pixel Office의 정체성은 유지한다. 주요 정보는 한국어로 읽을 수 있어야 한다.

## 3. 6단계 진행과 상태

인력계획 → 인재 정의 → 채용 설계 → 지원자 검증 → 인재 확보 → 업무 준비.
상단 또는 왼쪽 상단에 고정한다. 이 진행도는 자유 공간 Navigation이 아니다.

| 상태 | 의미와 행동 |
|---|---|
| 현재 | 지금 진행하는 Stage. 가장 강하게 표시 |
| 완료 | 이미 탐색한 Stage. Summary 재확인 가능 |
| 예정 | 이후 Stage. Jump 불가 |

완료는 탐색 진행 상태이지 채용 성공이나 목표 달성 판정이 아니다.
완료 Summary 재확인은 실제 진행 위치·정본 결과를 되돌리지 않는다.
지도·단계 목록·Mission Board의 다른 진입점도 예정 Stage 이동 제한을 우회하지 않는다.
V1의 UPCOMING 자유 이동과 방=Step 진행도는 대체한다.
Mission 2는 계획 확정에서 끝나므로 6단계의 구체적 적용은 OPEN-02다. 미수행 채용 실행 단계를 완료로 표시하지 않는다.

## 4. 공간과 Scene

기본 공간은 인력계획실 / 채용전략실 / 채용운영실 / 평가회의실 / 면접실 / 업무공간 / 데이터랩이다.
지원자 화면과 온라인 평가 화면은 상시 방이 아닌 특수 Scene Mode다.
Talent Desk는 채용전략실의 인재 요건 Workshop에 흡수하고 Onboarding은 업무공간에서 진행한다.
Mission Board는 요청·목표·Mission 전환을 담당하는 공통 요소이며 별도 업무 Stage가 아니다.

Room은 업무 장소, Stage는 진행 단계, Scene은 하나의 핵심 질문을 다루는 경험 단위다.
하나의 공간을 여러 Scene이 재사용한다. Scene 시작은 질문 → Human Activity → Evidence/Data
→ Interaction → 판단 → 결정 → 상태 전이 → 다음 질문 순서다.
[06 Scene Contract](06_mission1_experience_specification.md#2-scene-contract)에 10개 항목을 기록한다.

## 5. Role Character와 대화

캐릭터는 정보 제공자·판단 책임자·논의 상대·지원자·영향받는 사람 중 업무 역할이 있을 때만 등장한다.
ICT 인사담당자, 채용담당자, 현업 채용책임자, ML 엔지니어, 인사 데이터 분석가,
온보딩 멘토, 지원자, 신규 입사자라는 역할명을 사용한다.
가상 한국 인명 대신 `ML 엔지니어 / 직무면접 참여`처럼 맥락을 붙일 수 있다.
온라인 응시 장면에 불필요하게 HR 캐릭터를 세우지 않는다.

사람의 대화에는 Typing Effect를 사용하지 않는다. 개념을 길게 강의하지 않고 업무와 질문으로 보여준다.
대화 길이와 캐릭터 좌표는 후속 표현 조정 사항이다. 캐릭터 이동·표정으로 합불이나 Ready를 암시하지 않는다.

## 6. Mission 진입과 인력계획

첫 화면 Office 위에 Mission Intro와 `Mission 시작`을 제공한다. 주요 CTA가 경쟁하지 않는다.
Mission 시작 → 새로운 인력 요청 → 요청서 확인 → Goal Briefing → 인력계획 시작을 유지한다.
Intro는 이름을 가진 dialog로 구현하고 Focus 이동·복원과 Escape를 지원한다.

요청서는 가상 AI/ML 조직, 신입 ML Engineer, 필요 인력 16 FTE, 업무 준비 목표 2027-09를 전달한다.
16 FTE는 전체 필요 인력이며 신규 채용 수가 아니다. 시나리오 가정 Badge를 제공한다.
Gap을 정답으로 먼저 알려주지 않는다. 이후 Current 12, 전입 +1, 전출 -1, 확정 입사 0을 확인하고
Forecast 12와 Gap 4를 계산한 뒤 신입 확보 방식의 근거와 대안을 본다.
Goal 질문은 인력 충분성·인재 요건·유치·검증·목표시점 Ready를 짧게 연결한다.
FTE·전입/전출·Ramp-up은 첫 등장에 한국어 뜻을 설명한다.

## 7. Interaction과 정보 공개

기본 A형은 Guided Exploration이다. 답변 → 관찰 → 기준 → 후속 질문 등 사고과정을 클릭으로 확인한다.
B형 Think Before Reveal은 Mission 1에서 약 5~7회 사용하며 원리를 생각한 뒤 근거를 보여준다.
선택은 점수·정답/오답·벌점·합격자 변경·분기 결과를 만들지 않는다.
후보자를 뽑거나 순위화하는 질문으로 바꾸지 않는다.

정보는 Primary → Secondary → Detail로 공개한다. 한 번에 긴 Matrix나 모든 Skill 상세를 펼치지 않는다.
이전 내용은 다시 읽을 수 있게 유지한다. 상세 Evidence를 모두 열어야 다음으로 가는 조건은 만들지 않는다.
Scene을 넘기는 행동과 현재 시스템 Reveal의 `전체 표시`는 구분한다.
시간 경과나 애니메이션 완료만으로 다음 Scene에 진입하지 않는다.

## 8. System Reveal과 숫자

Workforce/Funnel/KPI 계산, 공고 점검, Evidence 검색, Dataset Loading, Python 작성·실행 결과에
빠른 순차 Reveal/Typing을 사용할 수 있다. 사용자는 언제든 전체 표시할 수 있다.
실제 처리와 표시 연출을 구분하고 없는 조회·실행에 가짜 성공 로그를 붙이지 않는다.
Reduced motion에서는 즉시 읽을 수 있게 한다.

Plan은 Plan SSOT, Actual은 canonical Dataset의 실제 계산 결과에서 가져온다.
Target·Actual·Derived·단위·기준일·표본·분모를 구분한다.
초기 Forecast 75%를 최종 Actual로, Join 목표 4명을 Ready 결과로 표시하지 않는다.
미연결 값은 준비 중/분석 결과 없음으로 표시하며 0·성공으로 채우지 않는다.

## 9. Decision Layer와 Evidence

기본 구조는 현재 질문 → 데이터/Evidence → 가정 → 판단 과정 → 결정 → 다음 질문이다.
이미 확인한 내용은 보존하고 주요 Decision에서 `판단 근거 보기`를 제공한다.
결정·이유·사용 데이터·공개 근거·검토 대안·재검토 조건을 탐색할 수 있게 한다.
사용자가 승인해서 Case 결과를 바꾼 것처럼 표현하지 않는다.

| 내부 유형 | UI 라벨 | Drill-down |
|---|---|---|
| PUBLIC | 공개자료 | 발행 주체·제목·원문·확인 범위·공식/아카이브 등 |
| INFERENCE | 직무 해석 | 해석과 기반 자료·원칙 |
| SYNTHETIC | 시나리오 가정 | Case/Event, 필드, 기간 |
| ANALYSIS | 데이터 분석 | Dataset 버전·입력·실제 코드·결과 항목 |

Badge는 색상 외 텍스트·형태로 구별한다. Summary → Source 추적을 제공한다.
AI 요약만 제공하지 않으며 원문 오류나 미확보도 표시한다. 출처 상태는 Evidence 유형과 별개다.

## 10. 채용 설계 화면

| 화면 | Human Layer / Interaction | Decision Layer |
|---|---|---|
| 인재 요건 Workshop | 현업과 HR이 업무→Skill→확인할 경험을 논의 | Must/Learnable/Plus 및 분류 근거 |
| 채용공고 | Editor 형태로 초안·실제 업무·인재 요건 연결 확인 | 공고 문장 근거와 사람이 확정한 내용 |
| 공고 점검 | 모호한 표현·내부용어·긴 문장·요건 혼재를 표시 | 제안·수정·사람의 확인 경계 |
| 지원자 화면 | Office dim, 공고·지원 문항·전형·지원 안내 탐색 후 HR 화면 복귀 | 내부 판단 패널을 축소하고 복귀 문맥 유지 |
| 인재 유치 | Target·Message·Content·Channel 논의 | 채널 선택 근거, 기대와 가정 |
| Funnel Planning | Gap→예상 전환→비용→가용시간→Trade-off를 회의와 모니터 계산으로 확인 | Target과 Capacity Plan의 근거 |
| Assessment Matrix | Skill→Evidence→주 평가·보완 평가를 단계적으로 펼침 | 방식·목적·중복 검증 방지 |

Funnel은 지원 시작 320 → 지원 완료 240 → 서류 통과 120 → 사전검증 통과 60
→ 1차면접 대상 20 → 2차면접 대상 8 → Offer 5 → Join 목표 4라는 계획이다.
v0.3은 1차 단일 Session 60분·3명 → 후보당 면접 3 person-hours,
20명 계획 → Initial 60 person-hours를 계산한다. Calibration은 필요시 별도로 표시한다. 사람의 검토를 거치며 '최적 20명'으로 단정하지 않는다.
숫자에 맞춰 통과시키는 quota로 표시하지 않는다. 상세 SSOT는 07이다.
공고 점검의 건수도 고정 예시를 실제 처리 결과로 쓰지 않는다. 가짜 Textio 점수·연동을 만들지 않는다.

## 11. 지원자 검증·평가 조정·최종 검토

지원자 01/02/03을 원본 답변·과제·관찰·관련 역량·후속 질문 순서로 탐색한다.
대표 사례는 Dataset v1 Freeze 후 별도 Mapping으로 연결한다. 07의 Pattern은 Desired Contrast이며 생성 입력이 아니다.
성적순 비교표를 만들지 않는다. 역량검사는 사전검증 내부 Activity 이벤트만 표현하고 실제 기업 문항을 아는 것처럼 표시하지 않는다.
기술평가와 AI 문제해결 과제는 1차면접 활동이다.

AI Skill 후보 → 사람의 연결 확정/수정/거부 → 사람의 Evidence 수준 기록을 구분한다.
수준은 확인되지 않음 / 제한적 / 충분 / 강함이며 0/1/2/3 점수로 바꾸지 않는다.
확인되지 않음은 역량 없음이 아니다. 관찰 원문과 판단 주체를 확인할 수 있어야 한다.
제품 사용자는 기록된 판단을 탐색하며 실지원자 평가자가 되는 것이 아니다.
원자료·관찰·판단은 모두 합성 시나리오임을 표시하며 실제 사람이 평가한 기록으로 표현하지 않는다.

평가 조정에서는 서로 다른 관찰과 원본 Evidence·Rubric을 함께 본다.
합의 / 의견 차이 남음 / 근거 부족을 표시하고 평균값으로 차이를 없애지 않는다.
최종 검토는 Evidence Coverage, Must 근거, 남은 불확실성, Learnable Gap, 조정 기록을 보여준다.
Coverage를 종합 역량 점수·AI 추천·순위로 바꾸지 않는다.

## 12. Offer / Join / Onboarding / Ready

최종검토→Offer→수락→입사와 거절·기한 만료·입사 전 철회를 구분한다.
확인된 사유만 표시하고 미확인 사유는 UNKNOWN이다.
JOINED ≠ READY를 명시한다. Selection Evidence→Skill Profile→Gap→Ramp-up→실제 업무 Evidence→사람의 Ready 확인을 연결한다.
1/3/6개월 업무와 연장 상태를 구분하고 멘토에게 목적에 필요한 업무 관련 정보만 전달한다.
Values 답변 원문·면접 인상·합불 논의를 온보딩 자료로 전부 넘기지 않는다.
상태의 의미는 07, 저장 계약은 09를 참조한다.

## 13. Mission 1 결과와 Mission 2

결과는 Workforce Outcome / Recruiting Process / Onboarding Outcome의 세 영역으로 나눈다.
Target과 실제 계산된 결과를 비교하되 단일 성공/실패 축하 화면을 만들지 않는다.
Mission 1은 WHAT만 설명하고 `데이터 분석 시작`으로 이어진다. 이상 징후도 실제 결과가 있을 때만 표시한다.

Mission 2는 새로운 경력 요청·Capability Gap 확인 뒤 Data Lab에서 이전 Dataset을 분석한다.
분석 질문 → 실제 Python 코드 표시 → 실행/계산 결과 → Table/Chart → 사실 → 가설 → 한계 → 다음 질문.
핵심 코드와 `전체 분석 코드 보기`를 제공한다. 표시 코드·결과·Dataset 버전이 일치해야 한다.
실시간 실행을 선택할지 사전 실행 산출물을 탐색할지는 OPEN-01이다.
사전 계산은 실제 코드로 생성한 경우에만 허용하며 그 재생을 실시간 실행처럼 표현하지 않는다.
가짜 코드·수작업 결과·고정 성공 로그를 금지한다.

분석할 때 Office를 억지로 화면에 유지하지 않고 질문·코드·표·차트에 적합한 Workspace로 전환할 수 있다.
Mission 문맥과 근거·Copilot은 유지한다. 관찰·가설·한계를 별도 구역으로 표시한다.
실제 분석 후 의미 있는 2~3개 패턴을 Main Story로 선택하고 나머지는 추가 분석으로 제공한다.

이후 신입/경력 조건을 비교하고 Office의 전략·평가 논의로 돌아온다.
Experience Evidence는 Technology→Context→Scale→Ownership→Decision→Problem→Action→Result를 탐색한다.
경력연수로 Capability를 점수화하지 않는다. 신입 전환율·Ramp-up을 그대로 복사하지 않는다.
마지막은 경력 인재 요건·Sourcing·Funnel·Capacity·Assessment·Target Join/Ready·측정 계획이다.
실제 경력채용이 끝났다는 UI를 만들지 않는다.

## 14. HR Tech와 Copilot

별도 AI 방·캐릭터 없이 Scene 내부의 도구로 제공한다. 기본 Copilot은 접혀 있으며 Primary CTA와 경쟁하지 않는다.
결론 → 근거 → 출처 → 불확실성으로 답한다. 근거가 없으면 `현재 제공된 데이터에서는 확인할 수 없습니다.`라고 한다.
정적·규칙 기반 설명으로 핵심 흐름을 제공할 수 있다. 외부 LLM을 추가해도 서버 측 호출만 허용한다.
공고 점검·지원 안내·평가 근거 정리·온보딩 지원·분석 보조의 권한은 08을 따른다.

## 15. Camera / Scroll / Motion

Office Camera는 현재 Scene의 장소·참여자·모니터를 안내한다.
Content Camera는 Case/Decision 본문 내부의 읽는 위치만 안내하며 브라우저 전체를 이동시키지 않는다.
Room→Character→Monitor→Decision/Interaction으로 주의를 연결하되 무작위 이동은 하지 않는다.

Panel은 Header / 독립 스크롤 본문 / Footer를 유지한다. 마지막 콘텐츠가 가려지지 않도록 여백을 둔다.
커서가 있는 영역의 입력을 우선하며 Panel wheel이 Office zoom을 일으키지 않는다.
Reveal 시 목표가 보이지 않으면 내부 스크롤로 안내하되 이미 보이면 생략한다.
사용자의 wheel·touch·키보드·드래그 입력은 진행 중인 자동 안내를 취소한다.
이전 내용은 보존하며 계속 아래로 끌어내리지 않는다.

Scene 전환은 클릭을 기준으로 상태·패널·진행도가 함께 갱신된다.
카메라·캐릭터 이동이 끝날 때까지 읽기나 입력을 잠그지 않는다.
연속 입력은 최신 의도를 따르며 이전 연출이 새 Scene을 덮지 않는다.
등장·Reveal·Chart 전환은 상태 이해에만 사용하고 반복 Bounce·긴 대기·성공 축하를 만들지 않는다.
V1의 고정 ms 값은 현재 구현 참고치이며 V2 필수 제품 계약이 아니다.

## 16. 언어·시각·접근성·화면 대응

Pixel/pastel 정체성과 원본 License/Credit을 유지한다. 본문 대비와 주요 Accent의 위계를 우선한다.
한국어 기본 라벨: 인력계획, 인재 요건, 채용공고, 인재 유치, 역량 검증, 기술평가, 평가 근거, 평가 조정, 최종 검토.
Python/Pandas/KPI/ML/Kafka/Spark 등 자연스러운 기술 용어는 유지할 수 있다.
제품은 독립 HR 업무 지원 목적만 설명한다.

키보드로 핵심 경로를 탐색하고 Focus를 볼 수 있어야 한다. 지도 드래그만으로 이동을 강제하지 않는다.
Tooltip은 Focus에서도 보이며 핵심 정보를 Tooltip에만 넣지 않는다.
모달은 이름·Focus 이동/가두기/복원·Escape를 지원하고 일반 옆 패널은 모달처럼 Focus를 가두지 않는다.
펼치기는 상태를 전달하고 색상 외 라벨로 상태·유형을 구분한다.
Reduced motion은 CSS와 코드 기반 이동 모두에 적용한다. Reveal Skip 후 정보 손실이 없어야 한다.

1920×1080과 일반 노트북을 우선한다. 모바일의 Office 전체 재현은 MVP 밖이지만 깨진 화면을 방치하지 않는다.
좁은 화면에서 본문·핵심 근거·현재 문맥을 우선하고 보조 영역을 접거나 세로 배치하며 Desktop 안내를 제공한다.
상세 breakpoint와 배치는 OPEN-13이다. 자료 없음·조회 실패·원문 오류를 영역별로 보여주고 전체 화면을 무한 로딩으로 막지 않는다.

## 17. V2 UX 수용 기준

아래는 후속 구현의 검증 조건이며 이번 문서 작업에서 통과했다는 뜻이 아니다.

| ID | 기준 |
|---|---|
| UX-01 | 첫 방문자가 Mission 시작과 다음 행동을 찾을 수 있다 |
| UX-02 | 요청→Goal→계산 순서이며 Gap/결론을 미리 공개하지 않는다 |
| UX-03 | Mission·Stage·Scene·공간·현재 질문이 같은 문맥을 가리킨다 |
| UX-04 | 6단계와 7공간을 구분하고 예정 단계 Jump를 모든 진입점에서 막는다 |
| UX-05 | 완료 Summary 재확인으로 진행·정본 결과가 변경되지 않는다 |
| UX-06 | Human Layer의 역할·업무와 Decision Layer의 근거가 연결된다 |
| UX-07 | 선택으로 합불·점수·순위·결과가 달라지지 않는다 |
| UX-08 | 네 Provenance, 출처 상태, Evidence Level을 혼동하지 않는다 |
| UX-09 | AI 후보/사람의 연결/평가/최종 판단을 구분하고 원문을 추적한다 |
| UX-10 | Plan과 Actual의 수치·단위·기간·산식이 canonical 자료와 일치한다 |
| UX-11 | JOINED/READY 및 미확인 사유/확인 사유를 구분한다 |
| UX-12 | Mission 1 WHAT→Mission 2 분석→경력 계획으로 이어진다 |
| UX-13 | 실제 코드·Dataset·결과가 일치하고 관찰·가설·한계를 구분한다 |
| UX-14 | 사람 대화에 Typing이 없고 시스템 Reveal은 Skip/reduced motion을 지원한다 |
| UX-15 | Panel 스크롤과 Office 입력이 분리되고 수동 입력이 안내 이동을 취소한다 |
| UX-16 | 키보드·Focus·dialog·정보 대비로 핵심 경로를 사용할 수 있다 |
| UX-17 | 없는 데이터가 0·완료·성공으로 표시되지 않는다 |
| UX-18 | 외부 AI API 없이 핵심 흐름이 동작하며 템플릿 Credit이 유지된다 |

V1 UX-13(예정 단계 자유 탐색)은 V2 UX-04/05로 대체했다.
예정 단계 이동 제한은 게임 점수 조건이 아니라 확정된 순차 탐색 규칙이다.

## 18. 남은 결정

OPEN-01 Python 실행 방식, OPEN-02 Mission 2 진행도 적용, OPEN-13 URL/재방문 복원·배치·모션 세부는
[11 Open Issues](11_v2_migration_specification.md#7-open-issues)에 기록한다.
이 미결정을 구현된 기능이나 승인된 상세 정책으로 표현하지 않는다.


### Mission 1 UI 연결 Implementation Note (2026-09-25)

사용자의 최신 UI 연결 요청에 따라 판단 패널은 왼쪽, 공간·사람은 오른쪽에 배치한다.
상위 6단계와 06의 M1-01~25를 사용한다. 22 Scene은 Capacity/HOLD 추가 이전 개수이며 축약하지 않는다.
판단 패널 Header/독립 스크롤/Footer, 기존 pastel/pixel·Credit을 유지한다.
URL의 mission/scene/case와 v1 전용 로컬 탐색 이력으로 새로고침·뒤로가기를 복원한다.
복원 위치는 이미 도달한 Scene까지 제한하며 저장소 접근 불가 시 현재 탭의 메모리 상태로 진행한다.
공간 탐색은 예정 업무 결과를 열지 않는다. 과거 Scene 재방문은 진행 최고 위치를 낮추지 않는다.
`node scripts/mission1-presentation.mjs`는 v1 hash를 확인하고 UI 전용 정적 projection만 만든다.
Dataset 생성이 아니며 npm dev/build 전 실행한다. Mapping과 정본은 읽기 전용이다.
6개 Think Before Reveal은 판단 원리를 생각한 후 저장된 근거를 공개하며 선택·점수·결과 분기를 만들지 않는다.
대표 근거는 Mapping의 Scene까지 누적 공개하며 미래 Final/Follow-up과 이후 Offer 상태를 앞당겨 보여주지 않는다.
사람 업무 맥락은 즉시 표시하고 시스템 기록의 타이핑은 전체 표시/reduced motion으로 생략 가능하다.
Mission 1 마무리는 탐색 완료만 기록하며 Mission 2 분석을 자동 실행하지 않는다.
