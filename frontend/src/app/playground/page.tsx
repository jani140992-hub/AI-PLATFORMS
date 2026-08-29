import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Send, SlidersHorizontal, Sparkles } from "lucide-react";

export default function PlaygroundPage() {
  return (
    <div className="h-[calc(100vh-8rem)] flex gap-6">
      <div className="flex-1 flex flex-col bg-white border border-gray-200 rounded-lg dark:border-gray-800 dark:bg-gray-950">
        <div className="h-14 border-b border-gray-200 px-6 flex items-center justify-between dark:border-gray-800">
          <div className="flex items-center space-x-3">
            <span className="font-semibold text-sm">Model:</span>
            <select className="border border-gray-200 rounded px-2 py-1 text-sm bg-white dark:bg-gray-900 dark:border-gray-700">
              <option>gpt-4o (OpenAI)</option>
              <option>claude-3-5-sonnet-20240620 (Anthropic)</option>
              <option>gemini-1.5-pro (Google)</option>
              <option>deepseek-chat (DeepSeek)</option>
            </select>
          </div>
          <Badge variant="success">Semantic Cache Active</Badge>
        </div>

        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs">U</div>
            <div className="bg-gray-100 p-4 rounded-lg text-sm max-w-xl dark:bg-gray-900">
              Compare the latency and cost tradeoffs between RAG with dense vector search versus hybrid search with BM25 and neural reranking.
            </div>
          </div>

          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-purple-600 text-white flex items-center justify-center font-bold text-xs">AI</div>
            <div className="bg-blue-50 border border-blue-100 p-4 rounded-lg text-sm max-w-2xl dark:bg-gray-900 dark:border-gray-800">
              <p className="font-medium text-blue-900 dark:text-blue-400 mb-2">OmniFlow Hybrid RAG Architecture Analysis:</p>
              <ul className="list-disc pl-5 space-y-1.5 text-gray-700 dark:text-gray-300">
                <li><strong>Dense Vector Search:</strong> Excellent semantic recall for conceptual inquiries; typical retrieval latency ~15-25ms.</li>
                <li><strong>Hybrid (Dense + BM25):</strong> Fuses exact keyword matching (SKUs, acronyms, code identifiers) with semantic embeddings via Reciprocal Rank Fusion (RRF); latency ~30-40ms.</li>
                <li><strong>Cross-Encoder Neural Reranking:</strong> Joint query-passage attention re-scoring; boosts P@1 precision by up to 28% with additional ~40-60ms overhead.</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          <div className="relative">
            <input
              type="text"
              placeholder="Ask a question or test model prompt..."
              className="w-full rounded-md border border-gray-200 pl-4 pr-24 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 dark:border-gray-700 dark:bg-gray-900"
            />
            <Button size="sm" className="absolute right-2 top-2 flex items-center">
              <Send className="w-3 h-3 mr-1" />
              Send
            </Button>
          </div>
        </div>
      </div>

      <div className="w-80 bg-white border border-gray-200 rounded-lg p-6 space-y-6 dark:border-gray-800 dark:bg-gray-950">
        <div className="flex items-center justify-between border-b pb-3">
          <h3 className="font-semibold text-sm flex items-center">
            <SlidersHorizontal className="w-4 h-4 mr-2" />
            Parameters
          </h3>
        </div>

        <div className="space-y-4 text-sm">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Temperature: 0.7</label>
            <input type="range" min="0" max="2" step="0.1" defaultValue="0.7" className="w-full" />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Max Tokens: 4096</label>
            <input type="range" min="256" max="8192" step="256" defaultValue="4096" className="w-full" />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">System Prompt</label>
            <textarea
              className="w-full border border-gray-200 rounded p-2 text-xs h-32 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:bg-gray-900 dark:border-gray-700"
              defaultValue="You are an enterprise AI architect operating within OmniFlow AI."
            />
          </div>
        </div>
      </div>
    </div>
  );
}
