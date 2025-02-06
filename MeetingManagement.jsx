import { useState } from "react";
import "./MeetingManagement.css";

function MeetingManagement() {
  const [agendaItems] = useState([
    { id: 1, title: "Q1 Financial Review", duration: "15m", progress: 80 },
    { id: 2, title: "Product Roadmap", duration: "30m", progress: 45 },
    { id: 3, title: "Team Feedback", duration: "20m", progress: 20 },
  ]);

  return (
    <div className="meeting-container">
      <div className="meeting-header">
        <h1>Meeting Dashboard</h1>
        <button className="new-meeting-btn">+ Schedule New Meeting</button>
      </div>

      <div className="meeting-timeline">
        <div className="timeline-header">
          <h2>Today's Agenda</h2>
          <div className="time-indicator">2:00 PM - 4:30 PM</div>
        </div>

        {agendaItems.map((item) => (
          <div key={item.id} className="agenda-item">
            <div className="agenda-progress">
              <div
                className="progress-bar"
                style={{ width: `${item.progress}%` }}
              ></div>
            </div>
            <div className="agenda-details">
              <h3>{item.title}</h3>
              <div className="agenda-meta">
                <span>⏱️ {item.duration}</span>
                <span>👥 12 participants</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="meeting-summary">
        <h2>Key Action Items</h2>
        <ul className="action-list">
          <li>✅ Finalize budget approval process</li>
          <li>📅 Schedule product demo with engineering</li>
          <li>📧 Send customer satisfaction survey</li>
        </ul>
      </div>
    </div>
  );
}

export default MeetingManagement;
