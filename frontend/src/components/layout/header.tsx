import React from "react";
import { Bell, Search, User } from "lucide-react";

export const Header: React.FC = () => {
  return (
    <header className="h-16 border-b border-gray-200 bg-white flex items-center justify-between px-6 dark:border-gray-800 dark:bg-gray-950">
      <div className="flex items-center w-96">
        <div className="relative w-full">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search agents, workflows, models, or docs..."
            className="w-full rounded-md border border-gray-200 pl-9 pr-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900"
          />
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button className="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
          <Bell className="w-5 h-5" />
        </button>
        <div className="flex items-center space-x-2 pl-2 border-l border-gray-200 dark:border-gray-800">
          <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-semibold text-sm">
            JD
          </div>
          <span className="text-sm font-medium">Jane Doe</span>
        </div>
      </div>
    </header>
  );
};
