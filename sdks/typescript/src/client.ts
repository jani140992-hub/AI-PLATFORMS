import {
  ChatCompletionRequest,
  ChatCompletionResponse,
  StreamChunk,
  RAGSearchResult,
  AgentExecutionResult,
} from "./types";

export interface OmniFlowOptions {
  apiKey: string;
  baseUrl?: string;
  timeout?: number;
}

export class OmniFlow {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;

  constructor(options: OmniFlowOptions) {
    this.apiKey = options.apiKey;
    this.baseUrl = (options.baseUrl || "http://localhost:8000").replace(/\/+$/, "");
    this.timeout = options.timeout || 60000;
  }

  private headers(): Record<string, string> {
    return {
      "Authorization": `Bearer ${this.apiKey}`,
      "X-API-Key": this.apiKey,
      "Content-Type": "application/json",
    };
  }

  public chat = {
    create: async (request: ChatCompletionRequest): Promise<ChatCompletionResponse> => {
      const resp = await fetch(`${this.baseUrl}/api/v1/chat/completions`, {
        method: "POST",
        headers: this.headers(),
        body: JSON.stringify({ ...request, stream: false }),
      });
      if (!resp.ok) {
        throw new Error(`OmniFlow API Error: ${resp.status} ${await resp.text()}`);
      }
      return resp.json() as Promise<ChatCompletionResponse>;
    },

    createStream: async function* (request: ChatCompletionRequest): AsyncGenerator<StreamChunk> {
      const resp = await fetch(`${this.baseUrl}/api/v1/chat/completions`, {
        method: "POST",
        headers: this.headers(),
        body: JSON.stringify({ ...request, stream: true }),
      });
      if (!resp.ok || !resp.body) {
        throw new Error(`OmniFlow Streaming Error: ${resp.status}`);
      }
      // Browser / Node stream reader simulation
      const text = await resp.text();
      const lines = text.split("\n");
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.substring(6).trim();
          if (dataStr === "[DONE]") break;
          try {
            const parsed = JSON.parse(dataStr);
            const delta = parsed.choices?.[0]?.delta?.content || "";
            yield { id: parsed.id, delta, finish_reason: parsed.choices?.[0]?.finish_reason };
          } catch {
            // continue
          }
        }
      }
    },
  };

  public rag = {
    query: async (params: { query: string; topK?: number }): Promise<RAGSearchResult[]> => {
      const resp = await fetch(`${this.baseUrl}/api/v1/rag/query`, {
        method: "POST",
        headers: this.headers(),
        body: JSON.stringify({ query: params.query, top_k: params.topK || 5 }),
      });
      if (!resp.ok) {
        throw new Error(`RAG Query failed: ${resp.status} ${await resp.text()}`);
      }
      return resp.json() as Promise<RAGSearchResult[]>;
    },
  };

  public agents = {
    execute: async (params: { prompt: string; mode?: "coordinator" | "consensus" }): Promise<AgentExecutionResult> => {
      const resp = await fetch(`${this.baseUrl}/api/v1/agents/execute`, {
        method: "POST",
        headers: this.headers(),
        body: JSON.stringify({ prompt: params.prompt, mode: params.mode || "coordinator" }),
      });
      if (!resp.ok) {
        throw new Error(`Agent Execution failed: ${resp.status} ${await resp.text()}`);
      }
      return resp.json() as Promise<AgentExecutionResult>;
    },
  };
}
