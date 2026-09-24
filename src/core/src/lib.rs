//! shared native foundation for airobloxbuilder.
//!
//! this crate intentionally stays platform-neutral. the windows and macos shells
//! can use it as the stable home for requests, agent state, and project events.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AiroRequest {
    pub text: String,
}

impl AiroRequest {
    pub fn new(text: impl Into<String>) -> Self {
        Self {
            text: text.into().trim().to_owned(),
        }
    }

    pub fn is_empty(&self) -> bool {
        self.text.is_empty()
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

/// classify the small set of built-in slash commands before model routing.
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
        assert_eq!(
            classify_command(&AiroRequest::new("/tasks")),
            BuilderCommand::Tasks
        );
    }

    #[test]
    fn ordinary_text_remains_a_message() {
        assert_eq!(
            classify_command(&AiroRequest::new("add a secret basement")),
            BuilderCommand::Message("add a secret basement".to_owned())
        );
    }
}
