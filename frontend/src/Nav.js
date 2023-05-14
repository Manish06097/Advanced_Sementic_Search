import React from 'react';

function Navbar() {
  return (
    <nav class="bg-white border-gray-200 dark:bg-[#141414] shadow-2xl">
      <div class="max-w-screen-xl mx-auto flex items-center justify-center p-4">
        <a  class="flex items-center">
          <img src="https://img.freepik.com/free-vector/cute-robot-holding-clipboard-cartoon-vector-icon-illustration-science-technology-icon-isolated_138676-5184.jpg?w=740&t=st=1683986556~exp=1683987156~hmac=74e1a090799a80b1160ad86b73f810ad3a3ef631c737adbbb5a6b351b11f60be" class="h-12 mr-3" alt="Flowbite Logo" />
          <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Semantic Search </span>
        </a>
      </div>
    </nav>
  );
}

export default Navbar;