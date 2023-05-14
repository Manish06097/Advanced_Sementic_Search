import React, { useState } from 'react';
import './App.css';
import Navbar from './Nav';
import SearchBar from './SearchBar';
import SearchButton from './SearchButton';
import UploadButton from './Upload';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [results, setResults] = useState([]);
  const handleChange = event => {
    setSearchTerm(event.target.value);
  }
  const handleClick = async (event) => {
    event.preventDefault();
    const response = await fetch('http://127.0.0.1:8000/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: searchTerm }),
    });

    if (response.ok) {
      const data = await response.json();
      setResults(data);
    } else {
      alert('Error performing search');
    }
  }
  return (
    <div>
      <div>
        <Navbar />
      </div>
      <div>
        <form class="flex items-center place-content-center py-5">   
          <SearchBar searchTerm={searchTerm} handleChange={handleChange} />
          <SearchButton handleClick={handleClick} />
        </form>
      </div>
      <UploadButton />
      <div class="flex flex-wrap justify-center py-10">
        
        {results.map((result, index) => (
          <div key={index} class=" rounded flex-col overflow-hidden shadow-lg m-4 bg-[#282828] w-4/6 my-2">
            <div class="px-6 py-2">
              <div class="font-bold text-xl mb-2 text-[#ECDBBA]">Result {index + 1}</div>
              <p class=" text-white text-base  font-thin">
               <span className='text-blue-300 font-semibold'>Context:- </span> {`${result['context']}`}
              </p>
              <p class=" text-white text-base py-2">
              <span className='text-green-300 font-semibold'>Name Entity:- </span> {`${result['Ner']}`}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
