import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar.jsx";
import Home from "./pages/Home.jsx";
import PersonalisedLearning from "./pages/PersonalisedLearning.jsx";
import AcademicPerformance from "./pages/AcademicPerformance.jsx";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <Navbar />
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-10">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/personalised-learning" element={<PersonalisedLearning />} />
          <Route path="/academic-performance" element={<AcademicPerformance />} />
        </Routes>
      </main>
      <footer className="border-t py-6 text-center text-xs text-slate-400">
        CampusPulse — built for smarter, calmer academics.
      </footer>
    </div>
  );
}
