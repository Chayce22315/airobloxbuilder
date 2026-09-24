#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TaskStatus { Pending, Working, Blocked, Complete, Skipped }
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AiroTask { pub id:String, pub title:String, pub status:TaskStatus, pub dependencies:Vec<String> }
impl AiroTask { pub fn new(id:impl Into<String>,title:impl Into<String>)->Self{Self{id:id.into(),title:title.into(),status:TaskStatus::Pending,dependencies:Vec::new()}} pub fn depends_on(mut self,id:impl Into<String>)->Self{self.dependencies.push(id.into());self} }