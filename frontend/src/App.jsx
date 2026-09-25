import { useState } from "react";
import ReactMarkdown from 'react-markdown';

function App({ apiUrl = "http://localhost:8000" }) {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! 👋 How can I help you find a hotel?"
    }
  ]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessage("");

    const newMessages = [
      ...messages,
      {
        role: "user",
        text: userMessage
      }
    ];

    setMessages(newMessages);

    try {
      // Map frontend 'text' to backend 'content' expected by FastAPI models
      const backendMessages = newMessages.map(msg => ({
        role: msg.role,
        content: msg.text
      }));

      const response = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ messages: backendMessages })
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: data.reply
        }
      ]);
    } catch (error) {
      console.error("Error connecting to chatbot backend:", error);
      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          text: "Sorry, I am having trouble connecting to the server right now."
        }
      ]);
    }
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
              <div key={index} className={`chat-message ${msg.role}`}>
                <strong>
                  {msg.role === "assistant"
                    ? "Hotel Assistant"
                    : "You"}
                  :
                </strong>
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
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