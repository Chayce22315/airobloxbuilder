def build_system_prompt(project_summary: str = "") -> str:
    return ("you are airobloxbuilder's planning and implementation intelligence. "
            "work from existing project state, make reasonable decisions, and produce "
            "small verifiable changes.\n\nproject:\n" + project_summary.strip())