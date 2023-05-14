import React, { useState } from 'react';

function UploadButton() {
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = async (event) => {
    setIsLoading(true);
    const file = event.target.files[0];
    const fileType = file.type;
    const validTypes = ["application/pdf", "text/plain"];

    if (validTypes.includes(fileType)) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch("http://127.0.0.1:8000/createDatabase", {
          method: 'POST',
          body: formData,
        });

        if(response.status === 200) {
          alert("File uploaded successfully.");
        } else {
          throw new Error("There was an error uploading the file.");
        }
      } catch (error) {
        alert("There was an error uploading the file.");
      }
    } else {
      alert("Invalid file type. Please upload PDF or TXT file.");
    }
    setIsLoading(false);
  };

    return (
    
    <div className='px-1  w-auto text-center '>
      <input class=" text-sm text-gray-900 border cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-[#3C3C3C] dark:border-[#3C3C3C] dark:placeholder-gray-400  " aria-describedby="file_input_help" id="file_input" type="file" onChange={handleFileChange} />
      <div className='inline-block'>
                <p className=" mt-1 text-xs text-gray-500 dark:text-gray-300" id="file_input_help">(Only .PDF and .TXT)</p>
      </div>
      {isLoading && <div>Loading...</div>}        
    </div>
    
  );
}

export default UploadButton;
