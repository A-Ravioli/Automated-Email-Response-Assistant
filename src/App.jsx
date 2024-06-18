// App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [response, setResponse] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async () => {
    const res = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Email Classifier</h1>
      </header>
      <div className="App-body">
        <textarea
          value={email}
          onChange={handleEmailChange}
          placeholder="Paste your email here..."
          rows="10"
          cols="50"
        ></textarea>
        <button onClick={handleSubmit}>Analyze Email</button>
        {response && (
          <div className="response">
            <h2>Response:</h2>
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
