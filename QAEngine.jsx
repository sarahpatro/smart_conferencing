import { useState } from "react";
import "./QAEngine.css";

function QAEngine() {
  const [activeQuestion, setActiveQuestion] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");

  const qaList = [
    {
      question: "What was decided about the marketing budget?",
      answer:
        "The team approved a 15% increase in Q2 marketing budget with focus on digital channels.",
    },
    {
      question: "Who's responsible for the product demo?",
      answer:
        "Sarah Johnson from Engineering will lead the product demo preparation.",
    },
  ];

  return (
    <div className="qa-container">
      <h1>Meeting Knowledge Base</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search meeting transcripts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button>🔍 Search</button>
      </div>

      <div className="qa-list">
        {qaList.map((qa, index) => (
          <div
            key={index}
            className={`qa-item ${activeQuestion === index ? "active" : ""}`}
            onClick={() =>
              setActiveQuestion(activeQuestion === index ? null : index)
            }
          >
            <div className="question">
              <div className="q-icon">❓</div>
              {qa.question}
            </div>
            {activeQuestion === index && (
              <div className="answer">
                <div className="a-icon">💡</div>
                {qa.answer}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default QAEngine;
