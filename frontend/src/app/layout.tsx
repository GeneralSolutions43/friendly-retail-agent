import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import ErudaProvider from "@/components/ErudaProvider";
import MinimalAgentOverlay from "@/components/MinimalAgentOverlay";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Friendly Retail Agent",
  description: "Your helpful shopping assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ErudaProvider>
          {children}
          <MinimalAgentOverlay />
        </ErudaProvider>
      </body>
    </html>
  );
}
