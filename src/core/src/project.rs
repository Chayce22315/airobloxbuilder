//! project state primitives shared by the native shells and orchestrator.

use std::path::PathBuf;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectSnapshot {
    pub name: String,
    pub root: PathBuf,
    pub revision: u64,
}

impl ProjectSnapshot {
    pub fn new(name: impl Into<String>, root: impl Into<PathBuf>) -> Self {
        Self {
            name: name.into(),
            root: root.into(),
            revision: 0,
        }
    }

    pub fn next_revision(&mut self) {
        self.revision = self.revision.saturating_add(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn revisions_are_monotonic() {
        let mut project = ProjectSnapshot::new("demo", "/tmp/demo");
        project.next_revision();
        project.next_revision();
        assert_eq!(project.revision, 2);
    }
}
