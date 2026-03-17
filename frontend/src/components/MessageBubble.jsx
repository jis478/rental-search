export default function MessageBubble({ role, content }) {
  return (
    <div className={`message ${role}`}>
      <div className="message-bubble">{content}</div>
    </div>
  );
}
