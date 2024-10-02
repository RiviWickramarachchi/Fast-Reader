import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');

  // Function to handle file selection
  const handleFileChange = (e) => {
    setFile(e.target.files[0]); // Store the selected file in the state
  };

  // Handle title input change
  const handleTitleChange = (e) => {
    setTitle(e.target.value);  // Update the title state with user input
  };

  // Function to handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file || !title) {
      setMessage("Please select a file and a title.");
      return;
    }

    // Create FormData object to send the file
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);

    try {
      // Make the POST request to the Django backend
      const response = await axios.post('http://127.0.0.1:8000/api/documents/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setMessage("File uploaded successfully!");
    } catch (error) {
      setMessage("Failed to upload file.");
    }
  };

  return (
    <div>
      <h2>File Upload</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" value={title} onChange={handleTitleChange} required/>
        <input type="file" onChange={handleFileChange} />
        <button className="btn" type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};


export default Home
