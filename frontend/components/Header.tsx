// frontend/components/Header.tsx
import Link from "next/link";
import React from "react";

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo / Site Title */}
        <div className="flex items-center">
          <Link href="/" className="text-2xl font-bold text-gray-800">
            FL Simulation
          </Link>
        </div>
        {/* Navigation Links */}
        <nav className="flex space-x-4">
          <Link
            href="/simulation"
            className="text-gray-600 hover:text-gray-800"
          >
            Simulation
          </Link>
          <Link
            href="/incentives"
            className="text-gray-600 hover:text-gray-800"
          >
            Incentives
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
