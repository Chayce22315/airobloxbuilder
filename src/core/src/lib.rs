//! shared native foundation for airobloxbuilder.
pub mod generation;
pub mod generator;
pub mod orchestrator;
pub mod graph;
pub mod workspace;
pub mod planner;
pub mod mcp;
pub mod model;
pub mod project;
pub mod system;
pub mod tasks;

pub use generator::GeneratedFile;
pub use planner::{BuildPlan,PlanItem};
pub use project::ProjectSnapshot;
pub use tasks::{AiroTask,TaskStatus};

#[derive(Debug,Clone,PartialEq,Eq)]
pub struct AiroRequest{pub text:String}
impl AiroRequest{pub fn new(text:impl Into<String>)->Self{Self{text:text.into().trim().to_owned()}} pub fn is_empty(&self)->bool{self.text.is_empty()}}
#[derive(Debug,Clone,Copy,PartialEq,Eq)]
pub enum AgentStatus{Idle,Working,Complete,Failed}
#[derive(Debug,Clone,PartialEq,Eq)]
pub enum BuilderCommand{Plan(String),Tasks,Test,Fix,Message(String)}
pub fn classify_command(request:&AiroRequest)->BuilderCommand{let text=request.text.trim();if let Some(rest)=text.strip_prefix("/plan"){return BuilderCommand::Plan(rest.trim().to_owned())}match text{"/tasks"=>BuilderCommand::Tasks,"/test"=>BuilderCommand::Test,"/fix"=>BuilderCommand::Fix,_=>BuilderCommand::Message(text.to_owned())}}
pub fn health()->&'static str{"airo core online"}
#[cfg(test)]mod tests{use super::*;#[test]fn commands_work(){assert_eq!(classify_command(&AiroRequest::new("/tasks")),BuilderCommand::Tasks);assert_eq!(classify_command(&AiroRequest::new("/plan mall")),BuilderCommand::Plan("mall".into()));}}