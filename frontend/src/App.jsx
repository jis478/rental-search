import { useState, useRef, useEffect } from "react";
import ChatInput from "./components/ChatInput";
import MessageBubble from "./components/MessageBubble";
import PropertyGrid from "./components/PropertyGrid";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSearch = async (query) => {
    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setLoading(true);

    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server error ${res.status}`);
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.message,
          listings: data.listings,
          searchParams: data.searchParams,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${err.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Rental Search</h1>
        <p>Search Australian rental properties with natural language</p>
      </header>

      <div className="messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>Try searching for properties like:</p>
            <ul>
              <li>"2 bed apartment in Richmond under $500/week"</li>
              <li>"Pet-friendly house in Brunswick with parking"</li>
              <li>"Studio near CBD under $400"</li>
            </ul>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i}>
            <MessageBubble role={msg.role} content={msg.content} />
            {msg.listings && msg.listings.length > 0 && (
              <PropertyGrid listings={msg.listings} />
            )}
            {msg.listings && msg.listings.length === 0 && (
              <p className="no-results">
                No properties found. Try broadening your search.
              </p>
            )}
          </div>
        ))}

        {loading && (
          <div className="loading">
            <div className="spinner" />
            <span>Searching properties...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSubmit={handleSearch} disabled={loading} />
    </div>
  );
}
