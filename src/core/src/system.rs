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