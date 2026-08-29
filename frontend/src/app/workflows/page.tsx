import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Play, GitBranch, Clock } from "lucide-react";

export default function WorkflowsPage() {
  const workflows = [
    {
      id: "wf-1",
      name: "Customer Sentiment & Action Router",
      desc: "Analyzes inbound support messages, categorizes urgency, and auto-generates draft ticket replies.",
      nodes: 5,
      version: "v2.1",
      lastRun: "2 mins ago",
    },
    {
      id: "wf-2",
      name: "Autonomous Deep Research Team",
      desc: "Supervisor agent dispatches 3 parallel web search workers and compiles consolidated research briefings.",
      nodes: 8,
      version: "v1.4",
      lastRun: "1 hour ago",
    },
    {
      id: "wf-3",
      name: "Contract Compliance & Redline Audit",
      desc: "Compares vendor agreements against corporate legal policies and highlights deviation clauses.",
      nodes: 6,
      version: "v3.0",
      lastRun: "Yesterday",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Graph Agent Workflows</h1>
          <p className="text-sm text-gray-500">Design, test, and orchestrate DAG multi-agent graphs.</p>
        </div>
        <Button className="flex items-center">
          <Plus className="w-4 h-4 mr-2" />
          Create Workflow
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {workflows.map((wf) => (
          <Card key={wf.id} className="flex flex-col justify-between hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="secondary">{wf.version}</Badge>
                <div className="text-xs text-gray-400 flex items-center">
                  <Clock className="w-3 h-3 mr-1" />
                  {wf.lastRun}
                </div>
              </div>
              <CardTitle>{wf.name}</CardTitle>
              <CardDescription>{wf.desc}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between pt-4 border-t border-gray-100 dark:border-gray-800">
                <div className="flex items-center text-xs text-gray-500">
                  <GitBranch className="w-4 h-4 mr-1 text-blue-600" />
                  {wf.nodes} Nodes
                </div>
                <div className="flex space-x-2">
                  <Button size="sm" variant="outline">Edit</Button>
                  <Button size="sm" className="flex items-center">
                    <Play className="w-3 h-3 mr-1" />
                    Run
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
