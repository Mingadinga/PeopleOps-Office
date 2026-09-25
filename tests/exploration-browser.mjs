// Browser smoke test using an isolated Chrome --remote-debugging-port=9223 session.
// Start the application on port 4173 before running this script. No extra dependency needed.
import assert from 'node:assert/strict';
import { writeFile } from 'node:fs/promises';
const targets = await fetch('http://127.0.0.1:9223/json/list').then(r => r.json());
const target = targets.find(item => item.type === 'page');
assert.ok(target, 'Chrome page target must exist');
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
let seq = 0;
const pending = new Map();
const errors = [];
const requests = [];
ws.onmessage = event => {
  const message = JSON.parse(event.data);
  if (message.id) {
    const entry = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) entry.reject(new Error(JSON.stringify(message.error)));
    else entry.resolve(message.result);
  }
  if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails.text);
  if (message.method === 'Network.requestWillBeSent') requests.push(message.params.request.url);
};
function send(method, params = {}) {
  return new Promise((resolve, reject) => { const id = ++seq; pending.set(id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params })); });
}
async function evaluate(expression) {
  const result = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description ?? result.exceptionDetails.text);
  return result.result.value;
}
async function until(expression) {
  for (let i = 0; i < 100; i++) {
    if (await evaluate(`Boolean(${expression})`)) return;
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  throw new Error(`Timeout: ${expression}`);
}
async function click(selector) {
  await evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
  await new Promise(resolve => setTimeout(resolve, 80));
}
async function screenshot(name) {
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  await writeFile(`/private/tmp/peopleops-${name}.png`, Buffer.from(shot.data, 'base64'));
}
try {
  await send('Page.enable'); await send('Runtime.enable'); await send('Network.enable');
  await send('Emulation.setDeviceMetricsOverride', { width:1440,height:1000,deviceScaleFactor:1,mobile:false });
  await send('Page.navigate',{url:'http://localhost:4173/'});
  await until('document.querySelector(".m1-app")');
  await evaluate('localStorage.clear()'); await send('Page.navigate',{url:'http://localhost:4173/'});
  await until('document.querySelector("dialog")?.open');
  assert.equal(await evaluate('document.activeElement.textContent.includes("Mission 시작")'),true);
  await screenshot('v2-intro');
  await click('.po-intro-cta');
  await until('document.querySelector(".m1-controls")');
  assert.equal(await evaluate('document.querySelectorAll("[data-stage]").length'),6);
  assert.equal(await evaluate('document.querySelectorAll("[data-room]").length'),7);
  assert.equal(await evaluate('document.querySelector("[data-stage]:last-child").disabled'),true);
  assert.equal(await evaluate('document.querySelector(".m1-panel-body").innerText.includes("인력 차이:")'),false);
  await screenshot('v2-office');
  const scene = () => evaluate('document.querySelector(".m1-panel .win-bar").innerText.match(/M1-[0-9]+/)?.[0]');
  const primary = () => click('.m1-controls .po-primary');
  async function progress(target) { for(let i=0;i<70 && await scene()!==target;i++) await primary(); assert.equal(await scene(),target); }
  async function revealAll() { for(let i=0;i<4;i++) { const text=await evaluate('document.querySelector(".m1-controls .po-primary")?.innerText'); if(/근거 확인|계산 근거|운영 판단|목표 브리핑/.test(text)) await primary(); else break; } }
  async function openCase(question) { await evaluate(`Array.from(document.querySelectorAll('.m1-case-questions button')).find(el=>el.textContent.includes(${JSON.stringify(question)})).click()`); await until('document.querySelector(".m1-case-trace")'); }
  async function showTrace() { await evaluate('(() => { const p=document.querySelector(".m1-panel-body"), t=document.querySelector(".m1-case-trace"); p.scrollTop+=t.getBoundingClientRect().top-p.getBoundingClientRect().top-20; })()'); }
  await progress('M1-12'); await revealAll();
  for(const text of ['60h','576h','516h','540h','600h']) assert.equal(await evaluate(`document.querySelector('[data-capacity]').innerText.includes(${JSON.stringify(text)})`),true);
  await screenshot('v2-capacity');
  await evaluate('document.querySelector(".m1-reveal button")?.click()');
  await until('document.querySelector(".m1-reveal button")===null');
  assert.equal(await evaluate('document.querySelector(".m1-reveal").innerText.includes("600h")'),true);
  await evaluate('document.querySelector(".m1-panel-body").scrollTop = document.querySelector(".m1-panel-body").scrollHeight');
  await screenshot('v2-capacity-decision');
  const currentScene=await scene();
  await click('[data-room="데이터랩"]'); assert.equal(await scene(),currentScene);
  assert.equal(await evaluate('document.querySelector(".m1-human").innerText.includes("아직 도달하지 않은")'),true);
  await click('[data-room="평가회의실"]');
  await progress('M1-14'); await openCase('근거가 부족하면');
  assert.equal(await evaluate('document.querySelectorAll(".m1-evidence-card").length'),3);
  assert.equal(await evaluate('document.querySelector(".m1-case-trace").innerText.includes("채용 진행 종료")'),false);
  await progress('M1-15'); await revealAll(); await openCase('근거가 부족하면');
  // Opening the case retains the thought/reveal state through repeated reveal.
  await revealAll(); await showTrace(); await screenshot('v2-c0003');
  assert.equal(await evaluate('document.querySelector("[data-case=C0003]").innerText.includes("판단 근거 대기")'),true);
  assert.equal(await evaluate('document.querySelector("[data-case=C0003]").innerText.includes("ML 역량이 부족")'),false);
  await progress('M1-17'); await openCase('추가 확인에도');
  assert.equal(await evaluate('document.querySelectorAll(".m1-evidence-card").length'),3);
  assert.equal(await evaluate('document.querySelectorAll("[data-final=DO_NOT_PROCEED]").length'),0);
  await progress('M1-18'); await openCase('추가 확인에도'); await showTrace(); await screenshot('v2-c0005-followup');
  assert.equal(await evaluate('document.querySelectorAll(".m1-evidence-card").length'),4);
  await progress('M1-19'); await revealAll(); await openCase('추가 확인에도'); await revealAll();
  assert.equal(await evaluate('document.querySelector("[data-final=DO_NOT_PROCEED]")!==null'),true);
  await evaluate('(() => { const p=document.querySelector(".m1-panel-body"), t=document.querySelector("[data-final=DO_NOT_PROCEED]"); p.scrollTop+=t.getBoundingClientRect().top-p.getBoundingClientRect().top-100; })()'); await screenshot('v2-c0005-decision');
  await openCase('평가자 의견이'); await revealAll();
  assert.equal(await evaluate('document.querySelector("[data-final=PROCEED_TO_OFFER]")!==null'),true);
  assert.equal(await evaluate('document.querySelectorAll(".m1-evidence-card").length'),3);
  assert.equal(await evaluate('document.querySelector(".m1-case-trace").innerText.includes("제안 기한 만료")'),false);
  await showTrace(); await screenshot('v2-c0228-followup');
  const before=await evaluate('document.querySelector(".m1-case-trace").innerText');
  await send('Page.reload'); await until('document.querySelector("[data-case=C0228]")');
  assert.equal(await evaluate('document.querySelector(".m1-case-trace").innerText'),before);
  await revealAll();
  await click('[data-room="인력계획실"]'); await click('[data-room="평가회의실"]');
  assert.equal(await evaluate('document.querySelector(".m1-case-trace").innerText'),before);
  await progress('M1-20');
  await evaluate('history.back()'); await until('document.querySelector("[data-case=C0228]")');
  assert.equal(await scene(),'M1-19');
  await progress('M1-23'); await revealAll();
  assert.equal(await evaluate('document.querySelector(".m1-panel-body").innerText.includes("JOINED ≠ READY")'),true);
  await screenshot('v2-ready');
  await progress('M1-24');
  assert.deepEqual(await evaluate('Array.from(document.querySelectorAll("[data-actual]")).map(el=>Number(el.textContent))'),[342,246,246,192,192,59,32,17]);
  for(const text of ['519h','57h'])assert.equal(await evaluate(`document.querySelector('.m1-panel-body').innerText.includes(${JSON.stringify(text)})`),true);
  await screenshot('v2-results');
  await progress('M1-25'); await primary();
  assert.equal(await evaluate('document.querySelector("[role=status]").innerText.includes("탐색 완료")'),true);
  await screenshot('v2-complete');
  // All breakpoints, keyboard, reduced motion and dialog dismissal.
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await click('[data-stage]:first-child');
  await until('document.querySelector(".m1-reveal button")===null');
  await evaluate('document.querySelector(".m1-header>button").focus()');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',text:'\r',windowsVirtualKeyCode:13});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  await until('document.querySelector("dialog")?.open');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  await until('!document.querySelector("dialog")');
  assert.equal(await evaluate('document.querySelector(".po-shell").inert'),false);
  for(const [width,height] of [[1920,1080],[1280,800],[390,844]]) {
    await send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:false});
    await new Promise(r=>setTimeout(r,200));
    assert.equal(await evaluate('document.documentElement.scrollWidth<=innerWidth'),true,`overflow ${width}`);
    assert.equal(await evaluate('document.querySelector(".m1-panel").getBoundingClientRect().right<=innerWidth'),true);
    await screenshot(`v2-${width}`);
  }
  assert.deepEqual(errors,[],'No uncaught browser errors');
  assert.equal(requests.some(url=>/\/api\//.test(url)),false);
  console.log('PASS: 25 scenes, six stages, seven rooms, v1 values, gated mapping traces, no future results, reload/back/revisit, keyboard, reduced motion, desktop/laptop/mobile, no API or browser errors.');
} catch(error) {
  console.error('Browser exceptions:',errors);
  console.error(await evaluate('document.body?.innerText.slice(0,2000)'));
  await screenshot('v2-failure'); throw error;
} finally { ws.close(); }
