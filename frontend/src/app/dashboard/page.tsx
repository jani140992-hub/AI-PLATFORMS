import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Activity, ArrowUpRight, Cpu, Database, Zap } from "lucide-react";

export default function DashboardPage() {
  const stats = [
    { title: "Total Requests (30d)", value: "1,420,892", change: "+14.2%", icon: Activity },
    { title: "Tokens Processed", value: "18.4M", change: "+8.7%", icon: Zap },
    { title: "Active Workflows", value: "34", change: "+4 new", icon: Cpu },
    { title: "Knowledge Bases", value: "12", change: "8,940 chunks", icon: Database },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Enterprise Overview</h1>
          <p className="text-gray-500 text-sm">Monitor multi-agent execution, gateway routing, and token metrics.</p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">Export Audit Log</Button>
          <Button>Deploy New Agent</Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-500">{stat.title}</CardTitle>
                <Icon className="w-4 h-4 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-green-600 mt-1 flex items-center">
                  <ArrowUpRight className="w-3 h-3 mr-1" />
                  {stat.change} from last month
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Recent Workflow Runs</CardTitle>
            <CardDescription>Real-time autonomous multi-agent execution stream</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-gray-100 dark:divide-gray-800">
              {[
                { name: "Financial Report Analyst", status: "completed", latency: "1.8s", tokens: "2,410" },
                { name: "Support Ticket Router", status: "completed", latency: "420ms", tokens: "680" },
                { name: "Code Review & Security Audit", status: "running", latency: "3.2s", tokens: "4,190" },
                { name: "RAG Document Ingestion Worker", status: "completed", latency: "890ms", tokens: "1,200" },
              ].map((run, i) => (
                <div key={i} className="py-3 flex items-center justify-between">
                  <div>
                    <div className="font-medium text-sm">{run.name}</div>
                    <div className="text-xs text-gray-400">{run.latency} • {run.tokens} tokens</div>
                  </div>
                  <Badge variant={run.status === "completed" ? "success" : "warning"}>
                    {run.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Gateway Provider Health & Latency</CardTitle>
            <CardDescription>Live circuit breaker and provider response times</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { provider: "OpenAI (GPT-4o)", status: "Healthy", latency: "240ms", success: "99.98%" },
                { provider: "Anthropic (Claude 3.5 Sonnet)", status: "Healthy", latency: "310ms", success: "99.95%" },
                { provider: "Google (Gemini 1.5 Pro)", status: "Healthy", latency: "290ms", success: "99.92%" },
                { provider: "DeepSeek (V3 Chat)", status: "Healthy", latency: "380ms", success: "99.89%" },
              ].map((p, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <div className="font-medium">{p.provider}</div>
                  <div className="flex items-center space-x-3 text-xs">
                    <span className="text-gray-500">{p.latency}</span>
                    <span className="text-green-600 font-semibold">{p.success}</span>
                    <Badge variant="success">{p.status}</Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
