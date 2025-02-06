import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css"; // Create this CSS file

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="brand-text">MeetGenius AI</span>
        <button
          className="menu-toggle"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle navigation"
        >
          ☰
        </button>
      </div>

      <ul className={`nav-links ${isMenuOpen ? "active" : ""}`}>
        <li>
          <NavLink to="/">Home</NavLink>
        </li>
        <li>
          <NavLink to="/upload">Upload Video</NavLink>
        </li>
        <li>
          <NavLink to="/meetings">Meetings</NavLink>
        </li>
        <li>
          <NavLink to="/translate">Translate</NavLink>
        </li>
        <li>
          <NavLink to="/qa">Q&A Engine</NavLink>
        </li>
      </ul>
    </nav>
  );
};

const NavLink = ({ to, children }) => (
  <Link
    to={to}
    className="nav-link"
    style={({ isActive }) => ({
      fontWeight: isActive ? "600" : "400",
      color: isActive ? "#fff" : "#e0e0e0",
    })}
  >
    {children}
  </Link>
);

export default Navbar;
