use crate::{AgentStatus, AiroRequest, BuilderCommand};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AgentPlan {
    pub agent: String,
    pub status: AgentStatus,
    pub reason: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Route {
    pub command: BuilderCommand,
    pub agents: Vec<AgentPlan>,
}

pub fn route(request: &AiroRequest) -> Route {
    let command = crate::classify_command(request);
    let agents = match &command {
        BuilderCommand::Plan(_) => vec![
            plan("orchestrator", "turn the request into a living implementation plan"),
            plan("gameplay", "identify gameplay systems"),
            plan("world", "identify world and map work"),
            plan("testing", "define acceptance tests"),
        ],
        BuilderCommand::Test => vec![plan("testing", "run project validation")],
        BuilderCommand::Fix => vec![
            plan("repair", "diagnose the current failure"),
            plan("testing", "verify the repair"),
        ],
        BuilderCommand::Tasks => vec![plan("orchestrator", "summarize the current task graph")],
        BuilderCommand::Message(_) => vec![plan("orchestrator", "interpret the request and select specialists")],
    };
    Route { command, agents }
}

fn plan(agent: &str, reason: &str) -> AgentPlan {
    AgentPlan { agent: agent.into(), status: AgentStatus::Idle, reason: reason.into() }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn plan_routes_to_multiple_specialists() {
        let route = route(&AiroRequest::new("/plan make a multiplayer game"));
        assert!(route.agents.iter().any(|a| a.agent == "world"));
        assert!(route.agents.iter().any(|a| a.agent == "testing"));
    }
}