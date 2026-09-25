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
  await send('Page.enable'); await send('Page.bringToFront'); await send('Runtime.enable'); await send('Network.enable');
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: 'http://localhost:4173/' });
  await until('document.querySelector("dialog")?.open');
  assert.equal(await evaluate('document.activeElement.textContent.includes("Mission 시작")'), true);
  assert.equal(await evaluate('document.querySelectorAll("[data-room]").length'), 6);
  assert.equal(await evaluate('document.querySelector(".po-shell").inert'), true);
  await screenshot('intro');
  await click('.po-intro-cta');
  await until('document.querySelector("[data-step=workforce]") && !document.querySelector("dialog")');
  assert.equal(await evaluate('document.querySelector("[data-room=workforce]").dataset.status'), 'CURRENT');
  assert.equal(await evaluate('document.querySelector(".po-guidance").textContent'), '여기서 시작하세요');
  assert.equal(await evaluate('document.querySelector(".po-case").innerText.includes("16") && document.querySelector(".po-case").innerText.includes("2027-09-01")'), true);
  for (const title of ['데이터 확인', '계산 과정 보기', '판단 근거 보기', '대안과 근거 보기']) {
    await evaluate(`Array.from(document.querySelectorAll('.po-disclosure-trigger')).find(el => el.textContent.trim().endsWith(${JSON.stringify(title)})).click()`);
  }
  assert.equal(await evaluate('document.querySelectorAll(".po-disclosure[data-open=true]").length'), 4);
  assert.equal(await evaluate('document.querySelector(".po-case").innerText.includes("12 + 1 − 1 = 12 FTE")'), true);
  // Collapse before capturing the normal reading layout.
  await evaluate('document.querySelectorAll(".po-disclosure[data-open=true] .po-disclosure-trigger").forEach(el => el.click())');
  await new Promise(resolve => setTimeout(resolve, 700));
  await screenshot('workforce');
  await click('.po-next .po-primary');
  await until('document.querySelector("[data-step=talent]")');
  assert.equal(await evaluate('document.querySelector("[data-room=workforce]").dataset.status'), 'REVIEWED');
  assert.equal(await evaluate('document.querySelector("[data-room=talent]").dataset.status'), 'CURRENT');
  assert.equal(await evaluate('document.querySelector(".po-location").innerText.includes("2 / 6")'), true);
  await screenshot('talent');
  // Upcoming rooms remain accessible, and skipping does not mark steps reviewed.
  await click('[data-room=onboarding]');
  await until('document.querySelector("[data-step=onboarding]")');
  assert.equal(await evaluate('document.querySelector("[data-room=talent]").dataset.status'), 'UPCOMING');
  await click('[data-room=workforce]');
  assert.equal(await evaluate('document.querySelector("[data-room=workforce]").innerText.includes("✓ 확인함")'), true);
  // Keyboard selection works independently of dragging / camera position.
  await evaluate('document.querySelector("[data-room=operations]").focus()');
  await until('document.activeElement?.dataset.room === "operations"');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', text: '\r', unmodifiedText: '\r', windowsVirtualKeyCode: 13 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 });
  await until('document.querySelector("[data-step=operations]")');
  await click('[data-room=attraction]');
  await until('document.querySelector("[data-step=attraction]")');
  await evaluate('Array.from(document.querySelectorAll(".po-header nav button")).find(el => el.textContent === "KPI").click()');
  await until('document.querySelector("[data-step=kpi]")');
  assert.equal(await evaluate('document.querySelector("[data-room=lab]").dataset.status'), 'UPCOMING');
  assert.equal(await evaluate('document.querySelector(".po-case").innerText.includes("KPI Actual · 분석 결과 없음")'), true);
  await click('[data-room=lab]');
  await until('document.querySelector("#lab-title")');
  assert.equal(await evaluate('document.querySelector(".po-location").innerText.includes("MISSION 02")'), true);
  await click('.po-case .po-primary');
  await until('document.querySelector("[data-step=kpi]")');
  await click('.po-next .po-primary');
  await until('document.querySelector("#board-title")');
  // Reduced motion bypasses both CSS pulse and JS camera interpolation.
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
  await send('Page.reload');
  await until('document.querySelector("dialog")?.open');
  assert.equal(await evaluate('getComputedStyle(document.querySelector(".po-intro-cta")).animationName'), 'none');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 });
  await until('!document.querySelector("dialog")');
  assert.equal(await evaluate('document.querySelector(".po-shell").inert'), false);
  await click('.po-board-panel .po-primary');
  await until('document.querySelector("[data-step=workforce]")');
  const transform = await evaluate('document.querySelector(".world-stage").style.transform');
  await new Promise(resolve => setTimeout(resolve, 100));
  assert.equal(await evaluate('document.querySelector(".world-stage").style.transform'), transform);
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 1, mobile: false });
  await new Promise(resolve => setTimeout(resolve, 150));
  assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth'), true, 'mobile viewport must not overflow');
  await screenshot('mobile');
  assert.equal(requests.some(url => /\/api\/(report|integrations)/.test(url)), false, 'no game API calls');
  assert.deepEqual(errors, [], 'no uncaught browser errors');
  console.log('PASS: Intro, 6 rooms, disclosures, next/reviewed, direct selection, keyboard, KPI/Data Lab separation, reduced motion, mobile layout, no game API calls.');
} catch (error) {
  console.error("Browser exceptions:", errors);
  console.error(await evaluate("document.body?.innerText.slice(0, 2000)"));
  await screenshot("failure");
  throw error;
} finally { ws.close(); }
