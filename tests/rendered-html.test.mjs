import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const { default: worker } = await import("../dist/server/index.js");
  return worker.fetch(new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} });
}

test("renders the Mission intro and accessible Office without DB or API credentials", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html/);
  const html = await response.text();
  assert.match(html, /<title>PeopleOps Office/);
  assert.match(html, /<dialog[^>]*aria-labelledby="intro-title"/);
  assert.match(html, /Machine Learning Engineer/);
  assert.match(html, /Mission 시작/);
  for (const id of ["workforce", "talent", "attraction", "operations", "onboarding", "lab"]) {
    assert.match(html, new RegExp(`data-room="${id}"`));
  }
  assert.match(html, /Mission Board 열기/);
  assert.match(html, /Mission 01 단계 선택/);
  assert.match(html, /© godseng.mom/);
  assert.doesNotMatch(html, /오늘 업무 시작하기|일시정지|재생 속도|보고 발행|이 콘텐츠 승인하기|ceo\.console/);
});
