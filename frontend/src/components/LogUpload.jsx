import { useState } from "react";
import API from "../services/api";

function LogUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await API.post(
        "/upload-log",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      alert(response.data.message);

      if (onUploadSuccess) {
        onUploadSuccess();
      }

    } catch (error) {
      console.error(error);
      alert("Upload failed");
    }
  };

  return (
    <div style={{ marginBottom: "30px" }}>
      <h2>Upload Security Log</h2>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        style={{
          marginLeft: "10px",
          padding: "8px 16px",
          cursor: "pointer",
        }}
      >
        Upload
      </button>
    </div>
  );
}

export default LogUpload;