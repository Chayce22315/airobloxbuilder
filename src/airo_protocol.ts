export type agent_status = "idle" | "working" | "complete" | "failed";

export interface builder_request {
  text: string;
  request_id?: string;
}

export interface agent_route {
  agent: string;
  status: agent_status;
  reason: string;
}

export interface builder_event {
  type: "request" | "route" | "progress" | "complete" | "error";
  request_id: string;
  message: string;
  agents?: agent_route[];
}
