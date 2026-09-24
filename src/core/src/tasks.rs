//! small, serializable task primitives for the living project plan.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TaskStatus {
    Pending,
    InProgress,
    Blocked,
    Complete,
    Skipped,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AiroTask {
    pub id: String,
    pub title: String,
    pub status: TaskStatus,
}

impl AiroTask {
    pub fn new(id: impl Into<String>, title: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            title: title.into(),
            status: TaskStatus::Pending,
        }
    }

    pub fn set_status(&mut self, status: TaskStatus) {
        self.status = status;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tasks_start_pending() {
        let task = AiroTask::new("foundation", "create project foundation");
        assert_eq!(task.status, TaskStatus::Pending);
    }
}
