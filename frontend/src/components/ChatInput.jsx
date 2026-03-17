import { useState } from "react";

export default function ChatInput({ onSubmit, disabled }) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed || disabled) return;
    onSubmit(trimmed);
    setQuery("");
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Describe what you're looking for..."
        disabled={disabled}
        autoFocus
      />
      <button type="submit" disabled={disabled || !query.trim()}>
        Search
      </button>
    </form>
  );
}
