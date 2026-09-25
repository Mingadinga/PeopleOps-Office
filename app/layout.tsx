import type { Metadata } from "next";
import "./globals.css";
import "./office.css";
import "./exploration.css";
import "./exploration/v2/mission1.css";

export const metadata: Metadata = {
  title: "PeopleOps Office — 근거 기반 HR 의사결정",
  description: "인력계획부터 채용, 온보딩까지 데이터와 판단 근거를 공간을 이동하며 탐색하는 HR 업무 공간",
  openGraph: {
    title: "PeopleOps Office",
    description: "문제와 근거를 따라 HR 의사결정 과정을 탐색하세요.",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
