import React, { useState } from "react";
import "./VideoUpload.css"; // Create this CSS file

const VideoUpload = () => {
  const [videoFile, setVideoFile] = useState(null);
  const [videoURL, setVideoURL] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleVideoUpload = (file) => {
    if (file) {
      setVideoFile(file);
      setVideoURL(URL.createObjectURL(file));
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("video/")) {
      handleVideoUpload(file);
    }
  };

  return (
    <div className="upload-container">
      <h2 className="upload-title">Upload Meeting Video</h2>

      <div
        className={`upload-dropzone ${isDragging ? "dragging" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept="video/*"
          id="videoInput"
          className="upload-input"
          onChange={(e) => handleVideoUpload(e.target.files[0])}
        />
        <label htmlFor="videoInput" className="upload-label">
          {videoFile ? videoFile.name : "Drag & Drop or Click to Upload"}
        </label>
      </div>

      {videoURL && (
        <div className="video-preview">
          <h3>Preview</h3>
          <div className="video-wrapper">
            <video controls className="preview-video">
              <source src={videoURL} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      )}
    </div>
  );
};

export default VideoUpload;
