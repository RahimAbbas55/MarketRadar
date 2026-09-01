import ReactMarkdown from "react-markdown";
import { useState, useRef, useEffect } from "react";
import "./App.css";

interface Message {
  role: "user" | "assistant" | "error";
  content: string;
}

const API_URL = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [activeTools, setActiveTools] = useState<string[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, activeTools]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setActiveTools([]);

    try {
      const response = await fetch(`${API_URL}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content }),
      });

      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const event = JSON.parse(line.slice(6));

          if (event.type === "tool_call") {
            setActiveTools((prev) => [...prev, event.tool]);
          } else if (event.type === "final_answer") {
            setMessages((prev) => [
              ...prev,
              { role: "assistant", content: event.content },
            ]);
            setActiveTools([]);
          }
        }
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "error",
          content:
            "Connection lost. Check that the backend is running and try again.",
        },
      ]);
      setActiveTools([]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const formatToolName = (tool: string) =>
    tool.replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase());

  return (
    <div className="app">
      <h1>MarketRadar</h1>
      <p className="subtitle">AI-powered investment research</p>
      <div className="messages">
        {messages.length === 0 && activeTools.length === 0 && (
          <div className="empty-state">
            Ask about a stock, or compare two — e.g. "Compare TSLA and RIVN"
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === "assistant" ? (
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            ) : (
              msg.content
            )}
          </div>
        ))}
        {activeTools.length > 0 && (
          <div className="trace">
            {activeTools.map((tool, i) => (
              <div key={i} className="trace-item">
                <span className="trace-dot" />
                Calling {formatToolName(tool)}...
              </div>
            ))}
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-area">
        <input
          ref={inputRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about a stock..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;