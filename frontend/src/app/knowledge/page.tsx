import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Database, UploadCloud, Search, FileText } from "lucide-react";

export default function KnowledgePage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Knowledge Bases (RAG)</h1>
          <p className="text-sm text-gray-500">Manage vector indices, document chunking pipelines, and hybrid search.</p>
        </div>
        <Button className="flex items-center">
          <UploadCloud className="w-4 h-4 mr-2" />
          Upload Documents
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          { name: "Enterprise Product Specs", docs: 45, chunks: 3420, store: "Qdrant", model: "text-embedding-3-small" },
          { name: "Engineering RFCs & Architecture", docs: 128, chunks: 8910, store: "Qdrant", model: "text-embedding-3-small" },
          { name: "Customer Support FAQ & Runbooks", docs: 310, chunks: 14200, store: "pgvector", model: "text-embedding-3-small" },
        ].map((kb, i) => (
          <Card key={i}>
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="default">{kb.store}</Badge>
                <span className="text-xs text-gray-400">{kb.docs} Documents</span>
              </div>
              <CardTitle>{kb.name}</CardTitle>
              <CardDescription>{kb.chunks.toLocaleString()} indexed vector chunks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-xs text-gray-500 mb-4">Embedding: {kb.model}</div>
              <Button variant="outline" size="sm" className="w-full flex items-center justify-center">
                <Search className="w-3 h-3 mr-2" />
                Query Knowledge Base
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
