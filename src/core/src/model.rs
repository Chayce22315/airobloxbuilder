#[derive(Debug,Clone,PartialEq,Eq)]
pub struct ModelConfig{pub provider:String,pub model:String,pub endpoint:Option<String>}
impl ModelConfig{pub fn external(provider:&str,model:&str)->Self{Self{provider:provider.into(),model:model.into(),endpoint:None}}}