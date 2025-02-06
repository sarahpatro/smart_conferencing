import { motion } from "framer-motion";
import "./Home.css";

function Home() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="home-page"
    >
      <div className="hero-section">
        <h1 className="hero-title">
          Transform Your Meetings with AI Intelligence
        </h1>
        <p className="hero-subtitle">
          Automated note-taking, smart summaries, and real-time insights
        </p>

        <motion.img
          src="https://source.unsplash.com/1600x900/?conference,boardroom"
          alt="AI-powered meeting"
          className="hero-image"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3 }}
        />

        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📝</div>
            <h3>Smart Note-taking</h3>
            <p>Automatic transcription and highlight detection</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI Analysis</h3>
            <p>Sentiment analysis and action item extraction</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🌐</div>
            <h3>Multi-language</h3>
            <p>Real-time translation for global teams</p>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default Home;
