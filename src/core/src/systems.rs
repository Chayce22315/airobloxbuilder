#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionState {
    Disconnected,
    Connecting,
    Connected,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OnboardingState {
    pub started: bool,
    pub setup_confirmed: bool,
    pub mcp_setup_attempted: bool,
    pub mcp_connected: bool,
    pub completed: bool,
}

impl Default for OnboardingState {
    fn default() -> Self {
        Self {
            started: false,
            setup_confirmed: false,
            mcp_setup_attempted: false,
            mcp_connected: false,
            completed: false,
        }
    }
}

impl OnboardingState {
    pub fn can_finish(&self) -> bool {
        self.setup_confirmed && self.mcp_setup_attempted
    }

    pub fn resume_step(&self) -> &'static str {
        if !self.started { "welcome" }
        else if !self.setup_confirmed { "setup" }
        else { "mcp-connection" }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct McpCapabilities {
    pub inspect_project: bool,
    pub modify_project: bool,
    pub read_scripts: bool,
    pub run_commands: bool,
    pub read_errors: bool,
    pub preview: bool,
}

impl Default for McpCapabilities {
    fn default() -> Self {
        Self {
            inspect_project: false,
            modify_project: false,
            read_scripts: false,
            run_commands: false,
            read_errors: false,
            preview: false,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BuilderState {
    pub connection: ConnectionState,
    pub onboarding: OnboardingState,
    pub mcp: McpCapabilities,
}

impl Default for BuilderState {
    fn default() -> Self {
        Self {
            connection: ConnectionState::Disconnected,
            onboarding: OnboardingState::default(),
            mcp: McpCapabilities::default(),
        }
    }
}
