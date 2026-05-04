import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { loadQuestions } from "../utils/loadQuestions";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function StudentDashboard() {
  const navigate = useNavigate();

  const [selected, setSelected] = useState(null);
  const [mastery, setMastery] = useState([]);

  const [modelType, setModelType] = useState("DKT");
  const [selectedSubject, setSelectedSubject] = useState("math");

  const [questionBank, setQuestionBank] = useState({});
  const [skillNames, setSkillNames] = useState({});

  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [quizQuestions, setQuizQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [quizFinished, setQuizFinished] = useState(false);
  const [usedQuestions, setUsedQuestions] = useState([]);

  const [correctCount, setCorrectCount] = useState(0);
  const [wrongCount, setWrongCount] = useState(0);
  const [showExplanation, setShowExplanation] = useState(false);

  const userEmail = localStorage.getItem("email");

  // 🔥 GROUP QUESTIONS
  const groupBySkill = (data) => {
    const grouped = {};
    const skillMap = {};

    data.forEach((q) => {
      if (!grouped[q.skill_id]) {
        grouped[q.skill_id] = [];
        skillMap[q.skill_id] = q.skill_name;
      }
      grouped[q.skill_id].push(q);
    });

    return { grouped, skillMap };
  };

  // 🔥 LOAD DATA
  useEffect(() => {
    const loadAll = async () => {
      const math = await loadQuestions("/data/math_questions.csv");
      const physics = await loadQuestions("/data/physics_questions.csv");
      const programming = await loadQuestions("/data/programming_questions.csv");

      const mathData = groupBySkill(math);
      const physicsData = groupBySkill(physics);
      const programmingData = groupBySkill(programming);

      setQuestionBank({
        math: mathData.grouped,
        physics: physicsData.grouped,
        programming: programmingData.grouped,
      });

      setSkillNames({
        math: mathData.skillMap,
        physics: physicsData.skillMap,
        programming: programmingData.skillMap,
      });

      generateQuiz("math", {
        math: mathData.grouped,
        physics: physicsData.grouped,
        programming: programmingData.grouped,
      });
    };

    loadAll();
  }, []);

  const getSkillName = (skillId) => {
    return skillNames[selectedSubject]?.[skillId] || null;
  };

  // 🔥 GENERATE QUIZ
  const generateQuiz = (subject, bank = questionBank) => {
    const subjectBank = bank[subject];
    if (!subjectBank) return;

    let allQuestions = [];
    Object.values(subjectBank).forEach((arr) => {
      allQuestions.push(...arr);
    });

    const fresh = allQuestions.filter((q) => !usedQuestions.includes(q.id));
    const shuffled = fresh.sort(() => 0.5 - Math.random());
    const selected10 = shuffled.slice(0, 10);

    setQuizQuestions(selected10);
    setCurrentIndex(0);
    setQuizFinished(false);
    setCurrentQuestion(selected10[0]);

    setCorrectCount(0);
    setWrongCount(0);
    setShowExplanation(false);
    setMastery([]);

    localStorage.setItem("sequence", JSON.stringify([]));
  };

  // 🔥 HANDLE NEXT
  const handleNext = async () => {
    if (selected === null) {
      alert("Select an answer");
      return;
    }

    const correct = selected === currentQuestion.correctIndex ? 1 : 0;

    const newCorrect = correctCount + (correct === 1 ? 1 : 0);
    const newWrong = wrongCount + (correct === 0 ? 1 : 0);

    setCorrectCount(newCorrect);
    setWrongCount(newWrong);
    setShowExplanation(true);

    let sequence = JSON.parse(localStorage.getItem("sequence") || "[]");
    sequence.push([currentQuestion.skill_id, correct]);
    localStorage.setItem("sequence", JSON.stringify(sequence));

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sequence,
          model: modelType,
          subject: selectedSubject,
        }),
      });

      const data = await res.json();

      if (!data?.mastery) {
        alert("Invalid server response");
        return;
      }

      setMastery(data.mastery[0]);
      setUsedQuestions((prev) => [...prev, currentQuestion.id]);

      setTimeout(async () => {
        const next = currentIndex + 1;

        // ✅ QUIZ FINISHED
        if (next >= 10) {
          setQuizFinished(true);
          setCurrentQuestion(null);

          try {
            await fetch("http://localhost:5000/save-result", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                email: userEmail,
                subject: selectedSubject,
                score: ((newCorrect / 10) * 100).toFixed(2),
                correct: newCorrect,
                wrong: newWrong,
                mastery: data.mastery[0] || [],
              }),
            });

            console.log("✅ Result saved");
          } catch (err) {
            console.error("❌ Save failed:", err);
          }

          return;
        }

        setCurrentIndex(next);
        setCurrentQuestion(quizQuestions[next]);
        setSelected(null);
        setShowExplanation(false);
      }, 800);

    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  };

  const changeSubject = (subject) => {
    setSelectedSubject(subject);
    generateQuiz(subject);
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/");
  };

  // 🔥 GRAPH DATA
  const chartData = mastery
    .map((m, i) => {
      const name = getSkillName(i);
      if (!name) return null;
      return {
        skill: name,
        mastery: Math.round(m * 100),
      };
    })
    .filter(Boolean);

  const getRecommendations = () => {
    return chartData
      .sort((a, b) => a.mastery - b.mastery)
      .slice(0, 3);
  };

  return (
    <div className="flex h-screen bg-[#0b1020] text-white">

      {/* SIDEBAR */}
      <div className="w-64 bg-[#0f172a] p-6 flex flex-col justify-between">
        <div>
          <h2 className="text-lg font-bold mb-6">Research Portal</h2>
          <p className="text-sm mb-3">{userEmail}</p>

          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value)}
            className="bg-gray-800 p-2 rounded w-full mb-6"
          >
            <option value="DKT">DKT</option>
            <option value="AKT">AKT</option>
          </select>

          <button onClick={() => changeSubject("math")} className="w-full mb-2 bg-purple-600 p-2 rounded">Math</button>
          <button onClick={() => changeSubject("physics")} className="w-full mb-2 bg-gray-700 p-2 rounded">Physics</button>
          <button onClick={() => changeSubject("programming")} className="w-full bg-gray-700 p-2 rounded">Programming</button>
        </div>

        <button onClick={handleLogout} className="bg-red-500 p-2 rounded">
          Logout
        </button>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-6">

        <h1 className="text-2xl font-bold mb-4">
          {selectedSubject.toUpperCase()} Dashboard
        </h1>

        {/* GRAPH */}
        {quizFinished && chartData.length > 0 && (
          <>
            <div className="bg-[#1e293b] p-4 rounded mb-4">
              <h3 className="mb-2 font-bold">Skill Mastery</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData}>
                  <XAxis dataKey="skill" stroke="#fff" />
                  <YAxis stroke="#fff" />
                  <Tooltip />
                  <Bar dataKey="mastery" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-[#1e293b] p-4 rounded mb-4">
              <h3 className="font-bold mb-2">Recommended Focus</h3>
              {getRecommendations().map((s, i) => (
                <p key={i} className="text-yellow-400">
                  {s.skill} → {s.mastery}%
                </p>
              ))}
            </div>
          </>
        )}

        {/* QUESTION */}
        {currentQuestion && !quizFinished && (
          <div className="bg-[#1e293b] p-6 rounded">
            <h2>Q{currentIndex + 1}/10: {currentQuestion.text}</h2>

            {currentQuestion.options.map((opt, i) => (
              <div key={i}
                onClick={() => setSelected(i)}
                className={`p-3 mb-2 cursor-pointer ${
                  selected === i ? "bg-purple-600" : "bg-[#0f172a]"
                }`}>
                {opt}
              </div>
            ))}

            <button onClick={handleNext}
              className="mt-4 bg-purple-600 px-6 py-2 rounded">
              Submit & Next
            </button>

            {showExplanation && (
              <div className="mt-4 text-green-400">
                {selected === currentQuestion.correctIndex ? "✅ Correct" : "❌ Wrong"}
                <p>{currentQuestion.explanation}</p>
              </div>
            )}
          </div>
        )}

        {/* RESULT */}
        {quizFinished && (
          <div className="bg-[#1e293b] p-6 rounded mt-6">
            <h2>Quiz Completed ✅</h2>
            <p>Correct: {correctCount}</p>
            <p>Wrong: {wrongCount}</p>
            <p>Score: {((correctCount / 10) * 100).toFixed(1)}%</p>

            <button onClick={() => generateQuiz(selectedSubject)}
              className="bg-green-500 px-6 py-2 rounded mt-4">
              Take Another Quiz
            </button>
          </div>
        )}
      </div>
    </div>
  );
}