import { useState } from "react";
import "./MultilingualAI.css";

function MultilingualAI() {
  const [selectedLanguage, setSelectedLanguage] = useState("en");
  const [text, setText] = useState("");

  const languages = [
    { code: "en", name: "English" },
    { code: "es", name: "Spanish" },
    { code: "fr", name: "French" },
    { code: "de", name: "German" },
  ];

  return (
    <div className="translation-container">
      <div className="language-selector">
        <h2>Real-time Translation</h2>
        <select
          value={selectedLanguage}
          onChange={(e) => setSelectedLanguage(e.target.value)}
          className="language-dropdown"
        >
          {languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>

      <div className="translation-boxes">
        <div className="translation-source">
          <h3>Original (English)</h3>
          <div className="message-bubble user">
            "Let's prioritize the Q2 marketing initiatives"
          </div>
        </div>

        <div className="translation-arrow">→</div>

        <div className="translation-target">
          <h3>
            Translation (
            {languages.find((l) => l.code === selectedLanguage)?.name})
          </h3>
          <div className="message-bubble bot">
            "Prioricemos las iniciativas de marketing del Q2"
          </div>
        </div>
      </div>

      <div className="translation-input">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type text to translate..."
          rows="4"
        />
        <button className="translate-btn">🌐 Translate</button>
      </div>
    </div>
  );
}

export default MultilingualAI;
