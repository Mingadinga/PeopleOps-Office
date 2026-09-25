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
  for (const id of ["인력계획실", "채용전략실", "채용운영실", "평가회의실", "면접실", "업무공간", "데이터랩"]) {
    assert.match(html, new RegExp(`data-room="${id}"`));
  }
  assert.match(html, /Mission Board 열기/);
  assert.match(html, /Mission 1 Scene 선택/);
  assert.match(html, /© godseng.mom/);
  assert.match(html, /data-dataset-version="v1"/);
  for (let i = 0; i < 6; i++) assert.match(html, new RegExp(`data-stage="${i}"`));
  assert.doesNotMatch(html, /오늘 업무 시작하기|일시정지|재생 속도|보고 발행|이 콘텐츠 승인하기|ceo\.console/);
});
