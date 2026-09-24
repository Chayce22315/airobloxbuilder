use std::path::{Path,PathBuf};
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct ProjectRoot(pub PathBuf);
impl ProjectRoot{
 pub fn new(path:impl Into<PathBuf>)->Self{Self(path.into())}
 pub fn is_directory(&self)->bool{Path::new(&self.0).is_dir()}
 pub fn join(&self,name:&str)->PathBuf{self.0.join(name)}
}
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct SystemCapability{pub id:String,pub available:bool}
pub fn capabilities()->Vec<SystemCapability>{vec![
 SystemCapability{id:"filesystem".into(),available:true},
 SystemCapability{id:"processes".into(),available:true},
 SystemCapability{id:"roblox-studio-mcp".into(),available:false},
]}

#[derive(Debug,Clone,Copy,PartialEq,Eq)]
pub enum ConnectionState{Disconnected,Connecting,Connected}

#[derive(Debug,Clone,Copy,PartialEq,Eq)]
pub struct OnboardingState{
 pub started:bool,
 pub setup_confirmed:bool,
 pub mcp_setup_attempted:bool,
 pub mcp_connected:bool,
 pub completed:bool,
}
impl Default for OnboardingState{
 fn default()->Self{Self{started:false,setup_confirmed:false,mcp_setup_attempted:false,mcp_connected:false,completed:false}}
}
impl OnboardingState{
 pub fn can_finish(&self)->bool{self.setup_confirmed&&self.mcp_setup_attempted}
 pub fn resume_step(&self)->&'static str{
  if !self.started{"welcome"} else if !self.setup_confirmed{"setup"} else{"mcp-connection"}
 }
}
