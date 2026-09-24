#[derive(Debug,Clone,PartialEq,Eq)]
pub struct GeneratedFile {
    pub path: String,
    pub contents: String,
}

impl GeneratedFile {
    pub fn new(path: impl Into<String>, contents: impl Into<String>) -> Self {
        Self { path: path.into(), contents: contents.into() }
    }
}
