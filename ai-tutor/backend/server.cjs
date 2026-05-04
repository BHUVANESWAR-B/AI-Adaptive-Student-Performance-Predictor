const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());
app.use(express.json());

/* =====================
   DATABASE CONNECTION
===================== */
const db = new sqlite3.Database("./database.db", (err) => {
  if (err) console.error(err.message);
  else console.log("✅ Connected to SQLite database");
});

/* =====================
   CREATE TABLES
===================== */

// USERS
db.run(`
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE,
  password TEXT,
  role TEXT
)
`);

// PER QUESTION ATTEMPTS
db.run(`
CREATE TABLE IF NOT EXISTS attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT,
  skill TEXT,
  correct INTEGER,
  model TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
`);

// 🔥 NEW: QUIZ RESULTS TABLE
db.run(`
CREATE TABLE IF NOT EXISTS quiz_results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT,
  subject TEXT,
  score REAL,
  correct INTEGER,
  wrong INTEGER,
  mastery TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
`);

/* =====================
   AUTH APIs
===================== */

// REGISTER
app.post("/register", (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).send("Missing fields");
  }

  db.run(
    "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
    [email, password, "student"],
    function (err) {
      if (err) {
        if (err.message.includes("UNIQUE")) {
          return res.status(400).send("User already exists");
        }
        return res.status(500).send(err.message);
      }
      res.send({ message: "User registered successfully" });
    }
  );
});

// LOGIN
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  db.get(
    "SELECT * FROM users WHERE email=? AND password=?",
    [email, password],
    (err, user) => {
      if (err) return res.status(500).send(err.message);

      if (user) res.send(user);
      else res.status(401).send("Invalid credentials");
    }
  );
});

/* =====================
   MODEL API PROXY
===================== */

app.post("/predict", async (req, res) => {
  try {
    const { sequence, model, subject } = req.body;

    const response = await axios.post("http://localhost:8000/predict", {
      sequence,
      model,
      subject,
    });

    res.send(response.data);

  } catch (err) {
    console.error("❌ Model Error:", err.message);
    res.status(500).send({ error: "Model error" });
  }
});

/* =====================
   STUDENTS (ADMIN)
===================== */

app.get("/students", (req, res) => {
  db.all(
    "SELECT id, email FROM users WHERE role='student'",
    [],
    (err, rows) => {
      if (err) return res.status(500).send(err.message);
      res.send(rows);
    }
  );
});

/* =====================
   ATTEMPTS (PER QUESTION)
===================== */

app.post("/attempt", (req, res) => {
  const { email, skill, correct, model } = req.body;

  db.run(
    "INSERT INTO attempts (email, skill, correct, model) VALUES (?, ?, ?, ?)",
    [email, skill, correct, model],
    function (err) {
      if (err) return res.status(500).send(err.message);

      res.send({ message: "Attempt saved" });
    }
  );
});

/* =====================
   🔥 QUIZ RESULTS (MAIN FEATURE)
===================== */

// SAVE FULL QUIZ RESULT
app.post("/save-result", (req, res) => {
  const { email, subject, score, correct, wrong, mastery } = req.body;

  if (!email || !subject) {
    return res.status(400).send("Missing fields");
  }

  db.run(
    `INSERT INTO quiz_results 
     (email, subject, score, correct, wrong, mastery)
     VALUES (?, ?, ?, ?, ?, ?)`,
    [
      email,
      subject,
      score,
      correct,
      wrong,
      JSON.stringify(mastery),
    ],
    function (err) {
      if (err) return res.status(500).send(err.message);

      res.send({ message: "Quiz result saved" });
    }
  );
});

// GET ALL RESULTS (ADMIN)
app.get("/results", (req, res) => {
  db.all("SELECT * FROM quiz_results ORDER BY timestamp ASC", [], (err, rows) => {
    if (err) return res.status(500).send(err.message);

    const parsed = rows.map((r) => ({
      ...r,
      mastery: JSON.parse(r.mastery || "[]"),
    }));

    res.send(parsed);
  });
});

/* =====================
   ANALYTICS
===================== */

// ALL ATTEMPTS
app.get("/analytics", (req, res) => {
  db.all("SELECT * FROM attempts", [], (err, rows) => {
    if (err) return res.status(500).send(err.message);
    res.send(rows);
  });
});

/* =====================
   DEV RESET
===================== */

app.delete("/reset", (req, res) => {
  db.run("DELETE FROM users");
  db.run("DELETE FROM attempts");
  db.run("DELETE FROM quiz_results");
  res.send("Database reset");
});

/* =====================
   START SERVER
===================== */

app.listen(5000, () => {
  console.log("🚀 Server running on http://localhost:5000");
});