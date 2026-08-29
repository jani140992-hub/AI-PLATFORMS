import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ShieldCheck, ShieldAlert, Lock, UserX } from "lucide-react";

export default function GuardrailsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Safety Guardrails & Governance</h1>
          <p className="text-sm text-gray-500">Configure PII scrubbing, prompt injection firewalls, and toxic content filters.</p>
        </div>
        <Button>Add Guardrail Policy</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Lock className="w-4 h-4 mr-2 text-blue-600" />
              PII Redaction Engine
            </CardTitle>
            <CardDescription>Automated detection and regex masking of sensitive entity records</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { name: "Social Security Numbers (SSN)", action: "Mask with [REDACTED_SSN]", active: true },
                { name: "Credit Card Numbers (PCI)", action: "Mask with [REDACTED_CREDIT_CARD]", active: true },
                { name: "Email Addresses & Phone", action: "Mask with [REDACTED_CONTACT]", active: true },
                { name: "API Keys & JWT Tokens", action: "Block Request", active: true },
              ].map((rule, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b text-sm">
                  <div>
                    <div className="font-medium">{rule.name}</div>
                    <div className="text-xs text-gray-400">{rule.action}</div>
                  </div>
                  <Badge variant="success">Active</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <ShieldAlert className="w-4 h-4 mr-2 text-red-600" />
              Prompt Injection & Jailbreak Firewall
            </CardTitle>
            <CardDescription>Real-time heuristic evaluation blocking adversarial system prompt overrides</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { name: "DAN & Role Reversal Defense", action: "Block & Alert", active: true },
                { name: "System Instruction Override Defense", action: "Block & Alert", active: true },
                { name: "Base64 Smuggling Inspector", action: "Decode & Inspect", active: true },
                { name: "Toxicity & Profanity Filter", action: "Mask Content", active: true },
              ].map((rule, i) => (
                <div key={i} className="flex items-center justify-between py-2 border-b text-sm">
                  <div>
                    <div className="font-medium">{rule.name}</div>
                    <div className="text-xs text-gray-400">{rule.action}</div>
                  </div>
                  <Badge variant="success">Active</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
