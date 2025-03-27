// // import { useState } from "react";
// // import axios from "axios";

// // const Chatbot = () => {
// //   const [input, setInput] = useState("");
// //   const [messages, setMessages] = useState([]);

// //   const sendMessage = async () => {
// //     if (!input.trim()) return;

// //     const userMessage = { sender: "user", text: input };
// //     setMessages((prevMessages) => [...prevMessages, userMessage]); // ✅ Append user message correctly

// //     try {
// //       const res = await axios.post("http://localhost:8000/api/chat/", { message: input });
// //       const botMessage = { sender: "bot", text: res.data.reply };
// //       setMessages((prevMessages) => [...prevMessages, botMessage]); // ✅ Append bot response correctly
// //     } catch (err) {
// //       console.error("Error:", err);
// //       setMessages((prevMessages) => [...prevMessages, { sender: "bot", text: "Error getting response" }]);
// //     }

// //     setInput("");
// //   };

// //   return (
// //     <div className="chat-container">
// //       <div className="chat-box">
// //         {messages.map((msg, i) => (
// //           <div key={i} className={msg.sender === "user" ? "user-msg" : "bot-msg"}>
// //             {msg.text}
// //           </div>
// //         ))}
// //       </div>
// //       <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type a message..." />
// //       <button onClick={sendMessage}>Send</button>
// //     </div>
// //   );
// // };

// // export default Chatbot;
// import React, { useState } from "react";
// import "./App.css";

// const Chatbot = () => {
//   const [messages, setMessages] = useState([
//     { text: "Hi there! How can I help you today?", sender: "bot" },
//   ]);
//   const [input, setInput] = useState("");

//   const sendMessage = () => {
//     if (!input.trim()) return;

//     const newMessages = [...messages, { text: input, sender: "user" }];
//     setMessages(newMessages);
//     setInput("");

//     // Simulate bot response
//     setTimeout(() => {
//       setMessages((prev) => [
//         ...prev,
//         { text: "This is a bot response.", sender: "bot" },
//       ]);
//     }, 1000);
//   };

//   return (
//     <div className="chat-container">
//       <div className="chat-header">Chatbot</div>
//       <div className="chat-messages">
//         {messages.map((msg, index) => (
//           <div key={index} className={`message ${msg.sender}`}>
//             {msg.text}
//           </div>
//         ))}
//       </div>
//       <div className="chat-input">
//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Type a message..."
//         />
//         <button onClick={sendMessage}>Send</button>
//       </div>
//     </div>
//   );
// };

// export default Chatbot;
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
      // Format response with line breaks and bold text
      let formattedText = res.data.reply
        .replace(/\n/g, "<br/>") // Line breaks
        .replace(/\*\*(.*?)\*\*/g, "<b>$1</b>"); // Convert **bold** to <b>bold</b>
  
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