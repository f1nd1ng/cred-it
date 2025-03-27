import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hi there! How can I help you today?", sender: "bot" },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
  
    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
  
    try {
      const res = await axios.post("http://localhost:8000/api/chat/", { message: input });
      console.log("API Response:", res.data.reply);
      let formattedText = res.data.reply
        .replace(/\n/g, "<br/>") 
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>"); 
  
      const botMessage = { sender: "bot", text: formattedText };
  
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (err) {
      setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: "Error getting response" }]);
    }
  
    setInput("");
  };
  
  return (
    <div className="chat-container">
      <div className="chat-header">Chatbot</div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`} dangerouslySetInnerHTML={{ __html: msg.text }}>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;