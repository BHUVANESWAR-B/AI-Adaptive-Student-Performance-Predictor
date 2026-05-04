import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function AdminDashboard() {
  const [students, setStudents] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [results, setResults] = useState([]);

  const [selectedStudent, setSelectedStudent] = useState("");

  // 🔥 LOAD DATA
  useEffect(() => {
    fetch("http://localhost:5000/students")
      .then((res) => res.json())
      .then((data) => {
        setStudents(data);
        if (data.length > 0) setSelectedStudent(data[0].email);
      });

    fetch("http://localhost:5000/analytics")
      .then((res) => res.json())
      .then(setAttempts);

    fetch("http://localhost:5000/results")
      .then((res) => res.json())
      .then(setResults);
  }, []);

  // 🔥 FILTER SELECTED STUDENT DATA
  const studentResults = results.filter(
    (r) => r.email === selectedStudent
  );

  // 🔥 GRAPH DATA (DATE + SCORE)
  const graphData = studentResults.map((r) => ({
    date: new Date(r.timestamp).toLocaleDateString(),
    score: r.score,
  }));

  // 🔥 SKILL STATS (GLOBAL)
  const skillStats = {};
  attempts.forEach((a) => {
    if (!skillStats[a.skill]) {
      skillStats[a.skill] = { total: 0, correct: 0 };
    }
    skillStats[a.skill].total++;
    skillStats[a.skill].correct += a.correct;
  });

  // 🔥 WEAK SKILLS
  const weakSkills = Object.entries(skillStats)
    .map(([skill, val]) => ({
      skill,
      accuracy: (val.correct / val.total) * 100,
    }))
    .filter((s) => s.accuracy < 60);

  return (
    <div className="flex h-screen bg-[#0b1020] text-white">

      {/* SIDEBAR */}
      <div className="w-64 bg-[#0f172a] p-6">
        <h2 className="text-lg font-bold mb-6">Admin Portal</h2>

        <p className="text-sm mb-3">Select Student</p>

        <select
          value={selectedStudent}
          onChange={(e) => setSelectedStudent(e.target.value)}
          className="w-full p-2 bg-gray-800 rounded"
        >
          {students.map((s) => (
            <option key={s.id} value={s.email}>
              {s.email}
            </option>
          ))}
        </select>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-6 overflow-y-auto">

        <h1 className="text-3xl font-bold mb-6">
          Student Performance Analytics
        </h1>

        {/* 🔥 GRAPH */}
        <div className="bg-[#1e293b] p-6 rounded mb-6">
          <h2 className="mb-4 text-xl">Performance Over Time</h2>

          {graphData.length === 0 ? (
            <p>No data available</p>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={graphData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#8b5cf6" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* 🔥 QUIZ HISTORY */}
        <div className="bg-[#1e293b] p-6 rounded mb-6">
          <h2 className="mb-4 text-xl">Quiz History</h2>

          {studentResults.length === 0 ? (
            <p>No quiz attempts</p>
          ) : (
            studentResults.map((r, i) => (
              <div key={i} className="mb-3 border-b border-gray-700 pb-2">
                <p>📅 {new Date(r.timestamp).toLocaleString()}</p>
                <p>📘 Subject: {r.subject}</p>
                <p>🎯 Score: {r.score}%</p>
                <p>✅ Correct: {r.correct}</p>
                <p>❌ Wrong: {r.wrong}</p>
              </div>
            ))
          )}
        </div>

        {/* 🔥 SKILL MASTERY */}
        <div className="mb-6">
          <h2 className="text-xl mb-3">Global Skill Mastery</h2>

          {Object.keys(skillStats).map((skill) => {
            const val = skillStats[skill];
            const acc = ((val.correct / val.total) * 100).toFixed(1);

            return (
              <div key={skill} className="mb-2">
                <p>{skill}</p>
                <div className="w-full bg-gray-700 h-2 rounded">
                  <div
                    className="bg-purple-500 h-2 rounded"
                    style={{ width: `${acc}%` }}
                  ></div>
                </div>
                <p className="text-sm text-gray-400">{acc}%</p>
              </div>
            );
          })}
        </div>

        {/* 🔥 WEAK SKILLS */}
        <div>
          <h2 className="text-xl mb-3 text-red-400">Weak Skills</h2>

          {weakSkills.length === 0 ? (
            <p>No weak skills 🎯</p>
          ) : (
            weakSkills.map((s, i) => (
              <p key={i}>
                {s.skill} ({s.accuracy.toFixed(1)}%)
              </p>
            ))
          )}
        </div>

      </div>
    </div>
  );
}