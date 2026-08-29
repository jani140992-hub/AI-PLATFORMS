import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Play, Award, BarChart2 } from "lucide-react";

export default function EvaluationsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Evaluations & LLM Benchmarks</h1>
          <p className="text-sm text-gray-500">Run standardized benchmarks and RAG Triad faithfulness evaluations.</p>
        </div>
        <Button className="flex items-center">
          <Play className="w-4 h-4 mr-2" />
          Run Evaluation Suite
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Award className="w-4 h-4 mr-2 text-amber-500" />
              MMLU Benchmark
            </CardTitle>
            <CardDescription>57 subjects across STEM, Humanities, and Social Sciences</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600">88.4%</div>
            <p className="text-xs text-gray-500 mt-1">Evaluated on GPT-4o • 1,200 samples</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart2 className="w-4 h-4 mr-2 text-green-500" />
              GSM8K Math Reasoning
            </CardTitle>
            <CardDescription>Multi-step mathematical grade school word problems</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">92.1%</div>
            <p className="text-xs text-gray-500 mt-1">Evaluated on Claude 3.5 Sonnet</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircle2 className="w-4 h-4 mr-2 text-indigo-500" />
              RAG Triad Composite Score
            </CardTitle>
            <CardDescription>Context Relevance + Groundedness + Answer Relevance</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-indigo-600">0.94 / 1.0</div>
            <p className="text-xs text-gray-500 mt-1">Zero hallucination violations detected</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
