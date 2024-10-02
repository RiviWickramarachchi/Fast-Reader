import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Home = () => {
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [docId, setDocId] = useState(null);
  const [wordList, setWordList] = useState([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const[currWord, setCurrWord] = useState('');
  const[isStarted,setIsStarted] = useState(false);

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
     console.log(response.data.content);
     setDocId(response.data.content);
     setMessage("File uploaded successfully!");
    } catch (error) {
      setMessage("Failed to upload file.");
    }
  };

  //Function to get the list of words in the pdf/doc file and display each word in the textbox
  const showWords = async (e) => {
    e.preventDefault();

    try{
        const response = await axios.get(`http://127.0.0.1:8000/api/documents/${docId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })


        //start displaying words
        setWordList(response.data.data);
        setIsStarted(true);



        //trigger the bool value to run the useEffect
        /*console.log(response.data.data);
        console.log("Word List " +wordList);*/

        //iterate through the arraylist
        
    }
    catch (error) {
    }
  };

  useEffect(() => {
    if (!isStarted) return; // If not started, return


    // Function to update the current word at each interval
    const wordInterval = setInterval(() => {
      if(currentWordIndex >= wordList.length)
      {
        //Stop displaying the words
        setIsStarted(false);
        return;
      }
      setCurrWord(wordList[currentWordIndex]); // Update the current word
      setCurrentWordIndex(prevIndex => prevIndex + 1); // Move to the next word
    }, 1000);

    // Cleanup the interval when the component is unmounted or the interval stops
    return () => clearInterval(wordInterval);
  }, [isStarted, currentWordIndex]);

  return (
    <div>
      <h2>File Upload</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="title">Title:</label>
        <input type="text" id="title" value={title} onChange={handleTitleChange} required/>
        <input type="file" onChange={handleFileChange} />
        <button className="btn" type="submit">Upload</button>
      </form>
      <br>
      </br>
      {message && <p>{message}</p>}
      <div>
        <br>
        </br>
        <button className="btn" onClick={showWords} >Read</button>
        <h3> Text Area </h3>
        <textarea id="txtbx" type="text" name="textbx" rows="4" cols="50" value={currWord} readOnly></textarea>
      </div>
    </div>

  );
};


export default Home
