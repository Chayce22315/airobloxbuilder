#[derive(Debug,Clone,PartialEq,Eq)]
pub struct McpCapability{pub name:String,pub description:String}
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct McpServer{pub name:String,pub connected:bool,pub capabilities:Vec<McpCapability>}
impl McpServer{pub fn disconnected(name:impl Into<String>)->Self{Self{name:name.into(),connected:false,capabilities:Vec::new()}}}