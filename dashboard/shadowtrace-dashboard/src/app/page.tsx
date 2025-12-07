// app/page.tsx

import Header from "../../components/Header";
import Hero from "../../components/Hero";

// import Header from '../components/Header';
// import Hero from '../components/Hero';
// import Features from '../components/Features';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-green-400 font-mono overflow-hidden">
      {/* Ensure the entire body is dark and uses a mono font */}
      <Header />
      <main>
        <Hero />
        {/* <Features /> */}
      </main>
    </div>
  );
}