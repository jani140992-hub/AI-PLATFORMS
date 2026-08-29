# @omniflow/sdk

Official TypeScript/JavaScript client SDK for the OmniFlow AI Platform. Works seamlessly in Node.js, Deno, Bun, and modern browsers.

## Installation

```bash
npm install @omniflow/sdk
```

## Usage

```typescript
import { OmniFlow } from "@omniflow/sdk";

const client = new OmniFlow({
  apiKey: process.env.OMNIFLOW_API_KEY || "your_api_key",
});

// Chat Completion
const completion = await client.chat.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Explain vector search." }],
});
console.log(completion.choices[0].message.content);

// Streaming
for await (const chunk of client.chat.createStream({
  model: "claude-3-5-sonnet-20240620",
  messages: [{ role: "user", content: "Write a short poem." }],
})) {
  process.stdout.write(chunk.delta);
}

// RAG Search
const results = await client.rag.query({
  query: "What is our refund policy?",
  topK: 3,
});
console.log(results);
```
