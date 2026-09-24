#[derive(Debug,Clone,PartialEq,Eq)]
pub struct PlanItem{pub id:String,pub title:String,pub depends_on:Vec<String>,pub status:String}
#[derive(Debug,Clone,PartialEq,Eq)]
pub struct BuildPlan{pub goal:String,pub items:Vec<PlanItem>}
pub fn make_plan(goal:impl Into<String>)->BuildPlan{let goal=goal.into().trim().to_owned();BuildPlan{goal:goal.clone(),items:vec![PlanItem{id:"foundation".into(),title:"create project foundation".into(),depends_on:vec![],status:"pending".into()},PlanItem{id:"gameplay".into(),title:format!("implement gameplay for {goal}"),depends_on:vec!["foundation".into()],status:"pending".into()},PlanItem{id:"testing".into(),title:"run automated checks".into(),depends_on:vec!["gameplay".into()],status:"pending".into()}]}}
#[cfg(test)]mod tests{use super::*;#[test]fn plan_has_dependencies(){let p=make_plan("infection game");assert_eq!(p.items.len(),3);assert_eq!(p.items[2].depends_on,vec!["gameplay"]);}}