export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'developer' | 'viewer';
}

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  plan: string;
  tokenQuota: number;
  tokensUsed: number;
}

export interface ModelOption {
  id: string;
  name: string;
  provider: string;
  contextWindow: number;
  inputCost: number;
  outputCost: number;
}

export interface WorkflowNode {
  id: string;
  type: 'llm' | 'tool' | 'condition' | 'human_approval' | 'router' | 'retriever';
  label: string;
  position: { x: number; y: number };
  config: Record<string, any>;
}

export interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  label?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  timestamp: string;
  toolCalls?: any[];
  tokens?: number;
}
