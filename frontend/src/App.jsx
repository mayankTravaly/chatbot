import { useState } from "react";

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! 👋 How can I help you find a hotel?"
    }
  ]);

  const sendMessage = () => {
    if (!message.trim()) return;

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        sender: "user",
        text: message
      }
    ]);

    setMessage("");
  };

  return (
    <>
      {isOpen && (
        <div className="chat-window">

          <div className="chat-header">
            Hotel Assistant
          </div>

          <div className="chat-body">
            {messages.map((msg, index) => (
              <p key={index}>
                <strong>
                  {msg.sender === "bot"
                    ? "Hotel Assistant"
                    : "You"}
                  :
                </strong>{" "}
                {msg.text}
              </p>
            ))}
          </div>

          <div className="chat-input">

            <input
              type="text"
              placeholder="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              Send
            </button>

          </div>

        </div>
      )}

      <button
        className="chat-button"
        onClick={() => {
          console.log("CHAT BUTTON CLICKED");
          setIsOpen((previous) => !previous);
        }}
      >
        💬
      </button>
    </>
  );
}

export default App;