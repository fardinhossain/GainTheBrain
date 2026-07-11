import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GainTheBrain — Idea Ledger",
  description: "A private, searchable reader for the project ideas your agent logs each day.",
};

const FONT_HREF =
  "https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&family=IBM+Plex+Mono:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href={FONT_HREF} rel="stylesheet" />
      </head>
      <body>{children}</body>
    </html>
  );
}
