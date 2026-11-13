import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadHistory() {
      try {
        const response = await fetch("/api/history/default");
        if (!response.ok) throw new Error("History unavailable");

        const data = await response.json();
        setMessages(data.messages || []);
      } catch (error) {
        console.error("Could not load history:", error);
      }
    }

    loadHistory();
  }, []);

  async function sendMessage(e) {
    e.preventDefault();

    if (!message.trim() || loading) return;

    const userMessage = message;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: userMessage },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMessage,
          session_id: "default",
        }),
      });

      if (!response.ok) throw new Error("Backend connection failed");

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.response },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: `Error: ${error.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header className="header">
        <h1>MACID_AI</h1>
        <span>LOCAL AI SYSTEM</span>
      </header>

      <section className="chat">
        {messages.length === 0 && (
          <div className="welcome">
            <h2>Welcome to MACID_AI</h2>
            <p>Your private local AI assistant.</p>
          </div>
        )}

        {messages.map((item, index) => (
          <div className={`message ${item.role}`} key={index}>
            <strong>{item.role === "user" ? "YOU" : "MACID_AI"}</strong>
            <p>{item.content}</p>
          </div>
        ))}

        {loading && <p className="loading">MACID_AI is thinking...</p>}
      </section>

      <form className="composer" onSubmit={sendMessage}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Message MACID_AI..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>SEND</button>
      </form>
    </main>
  );
}

export default App;
