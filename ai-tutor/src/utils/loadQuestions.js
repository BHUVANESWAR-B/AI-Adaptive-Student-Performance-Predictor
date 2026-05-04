import Papa from "papaparse";

export const loadQuestions = async (file) => {
  try {
    const res = await fetch(file);

    if (!res.ok) {
      throw new Error(`Failed to load file: ${file}`);
    }

    const text = await res.text();

    return new Promise((resolve, reject) => {
      Papa.parse(text, {
        header: true,
        skipEmptyLines: true, // 🔥 remove empty rows

        complete: (results) => {
          try {
            const data = results.data
              .map((q, index) => {
                // 🔥 VALIDATION (skip bad rows)
                if (!q.question_id || !q.question_text) return null;

                const correctMap = ["A", "B", "C", "D"];

                let correctIndex = correctMap.indexOf(
                  String(q.correct_option).toUpperCase()
                );

                if (correctIndex === -1) correctIndex = 0; // fallback

                return {
                  id: q.question_id.trim(),
                  subject: q.subject?.toLowerCase().trim(),
                  skill_id: parseInt(q.skill_id) || 0,
                  skill_name: q.skill_name || "Unknown",
                  difficulty: q.difficulty?.toLowerCase() || "easy",

                  text: q.question_text,

                  options: [
                    q.option_a,
                    q.option_b,
                    q.option_c,
                    q.option_d,
                  ].map((opt) => opt?.trim() || ""),

                  correctIndex,
                  explanation: q.explanation || "No explanation available",
                };
              })
              .filter(Boolean); // 🔥 remove null rows

            console.log(`✅ Loaded ${data.length} questions from ${file}`);

            resolve(data);
          } catch (err) {
            console.error("Parsing error:", err);
            reject(err);
          }
        },

        error: (err) => {
          console.error("PapaParse error:", err);
          reject(err);
        },
      });
    });
  } catch (err) {
    console.error("Fetch error:", err);
    return [];
  }
};