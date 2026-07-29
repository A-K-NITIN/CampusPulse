const BASE_URL = import.meta.env.VITE_API_BASE_URL;
const USE_MOCK = !BASE_URL;

const MOCK_RISK = {
  "Data Structures": { risk: "high", marks_pct: 42.0, attendance_pct: 61.0 },
  "Operating Systems": { risk: "medium", marks_pct: 58.0, attendance_pct: 74.0 },
  "Computer Networks": { risk: "low", marks_pct: 81.0, attendance_pct: 92.0 },
};

const MOCK_PLAN = {
  "Data Structures": {
    risk: "high",
    plan_text: "1. Arrays & recursion basics — needed before trees.\n2. Trees — prerequisite for graphs.\n3. Graphs — exam-critical, do last with most practice.",
    topics: ["Arrays & Recursion", "Trees", "Graphs"],
  },
  "Operating Systems": {
    risk: "medium",
    plan_text: "1. CPU Scheduling — foundational.\n2. Deadlocks — builds on scheduling concepts.",
    topics: ["CPU Scheduling", "Deadlocks"],
  },
};

const MOCK_INTENSITY = {
  "Data Structures": { risk: "high", hours_per_week: 8, days_per_week: 5, session_minutes: 96 },
  "Operating Systems": { risk: "medium", hours_per_week: 5, days_per_week: 4, session_minutes: 75 },
};

const MOCK_RESOURCES = {
  "Data Structures": {
    Trees: [{ content: "DS Trees — notes covering BST, AVL, traversals.", metadata: { type: "notes", file: "ds_trees_notes.txt" } }],
    Graphs: [{ content: "DS Graph — video walkthrough of BFS/DFS.", metadata: { type: "video", file: "ds_graph_video.txt" } }],
  },
};

const MOCK_REVISION = {
  backlog: [
    { subject: "Data Structures", topic: "Graphs", exam_date: "2026-08-10", risk_rank: 1 },
    { subject: "Operating Systems", topic: "Deadlocks", exam_date: "2026-08-14", risk_rank: 2 },
  ],
  revision_text: "Prioritize Graphs first — earliest exam date and highest risk. Then Deadlocks.",
};

async function getJSON(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export async function fetchRiskProfile(rollNo) {
  if (USE_MOCK) return MOCK_RISK;
  return getJSON(`/api/students/${rollNo}/risk`);
}

export async function fetchRecoveryPlan(rollNo) {
  if (USE_MOCK) return MOCK_PLAN;
  return getJSON(`/api/students/${rollNo}/recovery-plan`);
}

export async function fetchIntensity(rollNo) {
  if (USE_MOCK) return MOCK_INTENSITY;
  return getJSON(`/api/students/${rollNo}/intensity`);
}

export async function fetchResources(rollNo) {
  if (USE_MOCK) return MOCK_RESOURCES;
  return getJSON(`/api/students/${rollNo}/resources`);
}

export async function fetchRevisionPlan(rollNo) {
  if (USE_MOCK) return MOCK_REVISION;
  return getJSON(`/api/students/${rollNo}/revision-plan`);
}
