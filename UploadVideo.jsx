import { useState } from "react";
import "./UploadVideo.css";

function UploadVideo() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    // Simulate upload delay
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsUploading(false);
    alert(`Successfully uploaded: ${file.name}`);
  };

  return (
    <div className="upload-container">
      <h1>Upload Meeting Recording</h1>

      <div className="upload-card">
        <div className="upload-header">
          <div className="upload-icon">📤</div>
          <h2>Drag & Drop Video File</h2>
          <p>Supported formats: MP4, MOV, AVI</p>
        </div>

        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />

        {file && (
          <div className="file-preview">
            <video controls className="preview-player">
              <source src={URL.createObjectURL(file)} />
            </video>
            <div className="file-details">
              <span>{file.name}</span>
              <span>{(file.size / 1000000).toFixed(2)} MB</span>
            </div>
          </div>
        )}

        <button
          onClick={handleUpload}
          className={`upload-btn ${isUploading ? "uploading" : ""}`}
          disabled={isUploading}
        >
          {isUploading ? "Uploading..." : "Start Analysis"}
          {isUploading && <div className="upload-spinner"></div>}
        </button>
      </div>
    </div>
  );
}

export default UploadVideo;
