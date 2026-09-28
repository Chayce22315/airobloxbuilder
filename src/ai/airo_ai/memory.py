from dataclasses import dataclass, field

@dataclass
class ProjectMemory:
    project_name: str
    decisions: list[str] = field(default_factory=list)
    known_issues: list[str] = field(default_factory=list)
    conventions: list[str] = field(default_factory=list)

    def add_decision(self, value: str) -> None:
        if value.strip() and value.strip() not in self.decisions:
            self.decisions.append(value.strip())

    def add_issue(self, value: str) -> None:
        if value.strip() and value.strip() not in self.known_issues:
            self.known_issues.append(value.strip())

    def context(self) -> str:
        sections = [f"project: {self.project_name}"]
        if self.decisions: sections.append("decisions: " + "; ".join(self.decisions))
        if self.known_issues: sections.append("known issues: " + "; ".join(self.known_issues))
        if self.conventions: sections.append("conventions: " + "; ".join(self.conventions))
        return "\n".join(sections)
