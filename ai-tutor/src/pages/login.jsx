import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [role, setRole] = useState("student");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // 🔥 HANDLE LOGIN / REGISTER
  const handleSubmit = async () => {
    if (!email || !password) {
      alert("Please fill all fields");
      return;
    }

    setLoading(true);

    const url = isRegister
      ? "http://localhost:5000/register"
      : "http://localhost:5000/login";

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const text = await res.text();

      let data;
      try {
        data = JSON.parse(text);
      } catch {
        alert("Invalid server response");
        setLoading(false);
        return;
      }

      // ❌ ERROR CASE
      if (!res.ok) {
        alert(data.message || "Login/Register failed");
        setLoading(false);
        return;
      }

      // ✅ REGISTER FLOW
      if (isRegister) {
        alert("✅ Registered successfully! Please login.");
        setIsRegister(false);
        setEmail("");
        setPassword("");
        setLoading(false);
        return;
      }

      // ✅ LOGIN FLOW
      localStorage.setItem("email", data.email);
      localStorage.setItem("role", data.role);

      // 🔥 ROLE VALIDATION
      if (role !== data.role) {
        alert(`⚠ You selected "${role}" but account is "${data.role}"`);
        setLoading(false);
        return;
      }

      // 🔥 REDIRECT
      if (data.role === "student") navigate("/student");
      else navigate("/admin");

    } catch (err) {
      console.error(err);
      alert("Backend server not running (port 5000)");
    }

    setLoading(false);
  };

  return (
    <div className="flex h-screen bg-gradient-to-br from-[#0a0f2c] to-[#020617] text-white">

      {/* LEFT SIDE */}
      <div className="w-1/2 flex flex-col justify-center px-16">
        <p className="text-sm text-blue-400 tracking-widest">
          RESEARCH PORTAL ACCESS
        </p>

        <h1 className="text-6xl font-bold mt-4 leading-tight">
          Knowledge <br />
          <span className="text-purple-400">Tracing Study</span>
        </h1>

        <p className="mt-6 text-gray-400 max-w-md">
          Access the cognitive modeling environment and track adaptive learning
          trajectories across multi-dimensional neural networks.
        </p>

        <div className="mt-10">
          <p className="text-gray-400 text-sm">ACTIVE ANALYSIS</p>
          <h2 className="text-3xl font-bold mt-2">1.2M+</h2>
          <p className="text-gray-400">Data points traced</p>
        </div>

        <button className="mt-8 border border-gray-500 px-6 py-2 rounded-full hover:bg-gray-800">
          Apply for Access
        </button>
      </div>

      {/* RIGHT SIDE */}
      <div className="w-1/2 flex justify-center items-center">
        <div className="bg-[#0f172a] p-10 rounded-2xl w-[400px] shadow-lg">

          {/* ROLE SWITCH */}
          <div className="flex mb-6">
            <button
              onClick={() => setRole("student")}
              className={`flex-1 py-2 rounded ${
                role === "student"
                  ? "bg-gray-700"
                  : "text-gray-400 hover:bg-gray-800"
              }`}
            >
              STUDENT
            </button>

            <button
              onClick={() => setRole("admin")}
              className={`flex-1 py-2 rounded ${
                role === "admin"
                  ? "bg-gray-700"
                  : "text-gray-400 hover:bg-gray-800"
              }`}
            >
              ADMIN
            </button>
          </div>

          {/* INPUTS */}
          <input
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full p-3 bg-gray-800 rounded mb-4 outline-none focus:ring-2 focus:ring-purple-500"
          />

          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            placeholder="Password"
            className="w-full p-3 bg-gray-800 rounded mb-4 outline-none focus:ring-2 focus:ring-purple-500"
          />

          {/* BUTTON */}
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-purple-600 py-3 rounded-lg hover:bg-purple-700 disabled:opacity-50 transition"
          >
            {loading
              ? "Processing..."
              : isRegister
              ? "Register"
              : "Login"}
          </button>

          {/* TOGGLE */}
          <p
            onClick={() => setIsRegister(!isRegister)}
            className="text-center text-gray-400 text-sm mt-4 cursor-pointer hover:text-white"
          >
            {isRegister
              ? "Already have an account? Login"
              : "New user? Register"}
          </p>
        </div>
      </div>
    </div>
  );
}