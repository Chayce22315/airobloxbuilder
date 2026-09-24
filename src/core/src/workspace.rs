use crate::project::{FileKind, ProjectSnapshot};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorkspaceChange {
    pub path: String,
    pub kind: FileKind,
    pub description: String,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct ChangeSet {
    pub changes: Vec<WorkspaceChange>,
}

impl ChangeSet {
    pub fn preview(&self) -> Vec<String> {
        self.changes.iter().map(|change| {
            format!("{}: {}", change.path, change.description)
        }).collect()
    }

    pub fn apply_to(&self, project: &mut ProjectSnapshot) {
        for change in &self.changes {
            project.add_file(change.path.clone(), change.kind);
        }
    }
}
