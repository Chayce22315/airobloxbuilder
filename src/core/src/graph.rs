use crate::tasks::{AiroTask, TaskStatus};

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct TaskGraph {
    pub tasks: Vec<AiroTask>,
}

impl TaskGraph {
    pub fn add(&mut self, task: AiroTask) -> bool {
        if self.tasks.iter().any(|existing| existing.id == task.id) {
            return false;
        }
        self.tasks.push(task);
        true
    }

    pub fn ready(&self) -> Vec<&AiroTask> {
        self.tasks.iter().filter(|task| {
            task.status == TaskStatus::Pending
                && task.dependencies.iter().all(|dep| {
                    self.tasks.iter().any(|candidate| candidate.id == *dep && candidate.status == TaskStatus::Complete)
                })
        }).collect()
    }

    pub fn is_complete(&self) -> bool {
        !self.tasks.is_empty() && self.tasks.iter().all(|task| {
            matches!(task.status, TaskStatus::Complete | TaskStatus::Skipped)
        })
    }
}
