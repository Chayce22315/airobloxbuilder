#[derive(Debug,Clone,PartialEq,Eq)]
pub struct SystemEvent { pub kind:String, pub payload:String }

#[derive(Default)]
pub struct EventBus { queue:Vec<SystemEvent> }

impl EventBus {
    pub fn publish(&mut self,event:SystemEvent){self.queue.push(event);}
    pub fn drain(&mut self)->Vec<SystemEvent>{std::mem::take(&mut self.queue)}
}
