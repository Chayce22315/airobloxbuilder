#[derive(Debug, Clone)]
pub struct AiroRequest {
    pub text: String,
}

#[derive(Debug, Clone)]
pub enum AgentStatus {
    Idle,
    Working,
    Complete,
    Failed,
}

pub fn health() -> &'static str {
    "airo core online"
}
