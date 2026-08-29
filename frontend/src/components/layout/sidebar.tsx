import React from "react";
import Link from "next/link";
import {
  LayoutDashboard,
  GitBranch,
  MessageSquare,
  BookOpen,
  FileCode2,
  CheckCircle2,
  ShieldAlert,
  Cpu,
  BarChart3,
  Settings,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const navItems = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Workflows", href: "/workflows", icon: GitBranch },
    { label: "Playground", href: "/playground", icon: MessageSquare },
    { label: "Knowledge Bases", href: "/knowledge", icon: BookOpen },
    { label: "Prompt Studio", href: "/prompts", icon: FileCode2 },
    { label: "Evaluations", href: "/evaluations", icon: CheckCircle2 },
    { label: "Guardrails & Safety", href: "/guardrails", icon: ShieldAlert },
    { label: "Model Hub", href: "/models", icon: Cpu },
    { label: "Observability", href: "/analytics", icon: BarChart3 },
    { label: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-gray-200 bg-gray-50 flex flex-col h-screen dark:border-gray-800 dark:bg-gray-900">
      <div className="h-16 flex items-center px-6 border-b border-gray-200 dark:border-gray-800">
        <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          OmniFlow AI
        </span>
        <span className="ml-2 text-xs font-semibold px-2 py-0.5 bg-blue-100 text-blue-800 rounded">Enterprise</span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center px-3 py-2 text-sm font-medium text-gray-700 rounded-md hover:bg-gray-100 hover:text-blue-600 dark:text-gray-300 dark:hover:bg-gray-800"
            >
              <Icon className="w-5 h-5 mr-3" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <div className="text-xs text-gray-500 dark:text-gray-400">Tenant: Acme Corp</div>
        <div className="text-xs text-gray-400 mt-1">Quota: 12.4M / 50M tokens</div>
        <div className="w-full bg-gray-200 h-1.5 rounded-full mt-1.5 dark:bg-gray-700">
          <div className="bg-blue-600 h-1.5 rounded-full w-1/4"></div>
        </div>
      </div>
    </aside>
  );
};
