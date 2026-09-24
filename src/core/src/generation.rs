#[derive(Debug,Clone,PartialEq,Eq)]
pub struct GenerationRequest{pub prompt:String,pub context:String}
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct GenerationArtifact{pub path:String,pub contents:String}
pub fn sanitize_path(path:&str)->Option<String>{
 let clean=path.replace('\\\\','/');
 if clean.starts_with('/')||clean.split('/').any(|p|p==".."||p.is_empty()){None}else{Some(clean)}
}