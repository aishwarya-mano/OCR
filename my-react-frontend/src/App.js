import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [analyzedText, setAnalyzedText] = useState('');

  const fileSelectedHandler = event => {
    setSelectedFile(event.target.files[0]);
  };

  const fileUploadHandler = () => {
    const fd = new FormData();
    fd.append('image', selectedFile);
    axios.post('http://localhost:5000/api/analyze', fd)
      .then(res => {
        setAnalyzedText(res.data.text);
      })
      .catch(err => {
        console.error('Error:', err);
      });
  };

  return (
    <div className="App">
      <input type="file" onChange={fileSelectedHandler} />
      <button onClick={fileUploadHandler}>Analyze Image</button>
      {analyzedText && (
        <div>
          <h2>Analyzed Text</h2>
          <pre>{analyzedText}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
