export type AgentStatus = "idle" | "working" | "complete" | "failed";

export interface BuilderRequest {
  id: string;
  text: string;
  projectId?: string;
}

export interface BuilderEvent {
  id: string;
  kind: string;
  payload: unknown;
}

export interface AgentUpdate {
  agent: string;
  status: AgentStatus;
  message?: string;
}
