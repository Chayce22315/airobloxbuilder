#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectSnapshot { pub name:String, pub revision:u64, pub files:Vec<ProjectFile> }
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectFile { pub path:String, pub kind:FileKind }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileKind { Script, Asset, Map, Audio, Ui, Test, Other }
impl ProjectSnapshot { pub fn new(name:impl Into<String>)->Self{Self{name:name.into(),revision:0,files:Vec::new()}} pub fn add_file(&mut self,path:impl Into<String>,kind:FileKind){self.files.push(ProjectFile{path:path.into(),kind});self.revision+=1;} }