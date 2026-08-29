export interface ChatMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  name?: string;
}

export interface ChatCompletionRequest {
  model: string;
  messages: ChatMessage[];
  temperature?: number;
  max_tokens?: number;
  stream?: boolean;
}

export interface ChatChoice {
  index: number;
  message: ChatMessage;
  finish_reason?: string;
}

export interface UsageInfo {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatCompletionResponse {
  id: string;
  created: number;
  model: string;
  choices: ChatChoice[];
  usage: UsageInfo;
}

export interface StreamChunk {
  id: string;
  delta: string;
  finish_reason?: string;
}

export interface RAGSearchResult {
  chunk_id: string;
  content: string;
  fused_score: number;
  dense_score: number;
  bm25_score: number;
  metadata: Record<string, any>;
}

export interface AgentExecutionResult {
  question?: string;
  individual_responses?: Array<{ model: string; response: string }>;
  consensus_output?: string;
  participating_models?: string[];
  final_output?: string;
}
