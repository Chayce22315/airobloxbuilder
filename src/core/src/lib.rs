//! shared native foundation for airobloxbuilder.

pub mod orchestrator;
pub mod project;
pub mod tasks;

pub use orchestrator::{route, AgentPlan, Route};
pub use project::ProjectSnapshot;
pub use tasks::{AiroTask, TaskStatus};

extern "C" {
    fn airo_hash_bytes(data: *const u8, length: usize) -> u64;
    fn airo_protocol_version() -> u32;
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AiroRequest {
    pub text: String,
}

impl AiroRequest {
    pub fn new(text: impl Into<String>) -> Self {
        Self { text: text.into().trim().to_owned() }
    }

    pub fn is_empty(&self) -> bool {
        self.text.is_empty()
    }

    pub fn fingerprint(&self) -> u64 {
        let bytes = self.text.as_bytes();
        unsafe { airo_hash_bytes(bytes.as_ptr(), bytes.len()) }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AgentStatus {
    Idle,
    Working,
    Complete,
    Failed,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BuilderCommand {
    Plan(String),
    Tasks,
    Test,
    Fix,
    Message(String),
}

pub fn classify_command(request: &AiroRequest) -> BuilderCommand {
    let text = request.text.trim();

    if let Some(rest) = text.strip_prefix("/plan") {
        return BuilderCommand::Plan(rest.trim().to_owned());
    }

    match text {
        "/tasks" => BuilderCommand::Tasks,
        "/test" => BuilderCommand::Test,
        "/fix" => BuilderCommand::Fix,
        _ => BuilderCommand::Message(text.to_owned()),
    }
}

pub fn protocol_version() -> u32 {
    unsafe { airo_protocol_version() }
}

pub fn health() -> &'static str {
    "airo core online"
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_text_is_trimmed() {
        assert_eq!(AiroRequest::new("  build a mall  ").text, "build a mall");
    }

    #[test]
    fn slash_commands_are_classified() {
        assert_eq!(
            classify_command(&AiroRequest::new("/plan make an infection game")),
            BuilderCommand::Plan("make an infection game".to_owned())
        );
        assert_eq!(classify_command(&AiroRequest::new("/tasks")), BuilderCommand::Tasks);
    }

    #[test]
    fn ordinary_text_remains_a_message() {
        assert_eq!(
            classify_command(&AiroRequest::new("add a secret basement")),
            BuilderCommand::Message("add a secret basement".to_owned())
        );
    }

    #[test]
    fn native_protocol_is_available() {
        assert_eq!(protocol_version(), 1);
        assert_ne!(AiroRequest::new("hello").fingerprint(), 0);
    }
}
