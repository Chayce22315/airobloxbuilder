import SwiftUI

@main
struct AiroRobloxBuilderApp: App {
    var body: some Scene {
        WindowGroup("airobloxbuilder") {
            ContentView().frame(minWidth: 1050, minHeight: 680)
        }
    }
}

struct ContentView: View {
    @State private var prompt = ""
    @State private var messages = ["builder: what are we building?"]

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                HStack(spacing: 10) { Text("◈ airobloxbuilder").font(.title2.weight(.semibold)); Text("native").font(.caption).padding(.horizontal,8).padding(.vertical,4).background(.green.opacity(0.12)).clipShape(Capsule()) }
                Spacer()
                Text("● native shell ready").foregroundStyle(.green)
            }.padding(.horizontal, 18).frame(height: 54)
            Divider()
            HStack(spacing: 0) {
                ProjectPane()
                Divider()
                ChatPane(messages: $messages, prompt: $prompt)
                Divider()
                AgentPane()
            }
            Divider()
            HStack {
                Text("free forever • native • windows first").foregroundStyle(.secondary)
                Spacer()
                Text("v0.1 foundation").foregroundStyle(.secondary)
            }.padding(.horizontal, 18).frame(height: 62)
        }
    }
}

struct ProjectPane: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("project").foregroundStyle(.secondary).bold()
            Text("📁 my game").bold().padding(.top, 14)
            Text("  ├─ scripts"); Text("  ├─ assets"); Text("  ├─ maps")
            Text("  ├─ audio"); Text("  ├─ ui"); Text("  └─ tests")
            Text("tasks").foregroundStyle(.secondary).bold().padding(.top, 20)
            Text("○ no active tasks").foregroundStyle(.secondary)
            Text("commands").foregroundStyle(.secondary).bold().padding(.top, 20)
            HStack(spacing: 6) { Text("/plan"); Text("/tasks"); Text("/test"); Text("/fix") }.font(.caption).foregroundStyle(.secondary)
            Spacer()
        }.padding(16).frame(width: 255, alignment: .topLeading).background(.quaternary.opacity(0.15))
    }
}

struct ChatPane: View {
    @Binding var messages: [String]
    @Binding var prompt: String

    var body: some View {
        VStack {
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 14) {
                    ForEach(Array(messages.enumerated()), id: \.offset) { _, message in
                        Text(message).frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
            }
            HStack {
                TextField("describe your game or tell the builder what to do...", text: $prompt)
                    .textFieldStyle(.roundedBorder).onSubmit(send)
                Button("➤", action: send)
            }
        }.padding(18)
    }

    private func send() {
        let value = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !value.isEmpty else { return }
        messages.append("you: \(value)")
        messages.append(value.hasPrefix("/plan")
            ? "builder: planning request queued. the planner will turn this into a living task graph."
            : value.hasPrefix("/tasks")
                ? "builder: task view is ready for live orchestrator state."
                : "builder: request accepted. routing is ready for the orchestrator.")
        prompt = ""
    }
}

struct AgentPane: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("🧠 agents").font(.title2.weight(.semibold))
            Text("orchestrator  ● ready").padding(.top, 12)
            VStack(alignment: .leading, spacing: 6) {
                Text("live work").font(.caption.bold()).foregroundStyle(.secondary)
                Text("💬 chat  ● available")
                Text("💻 code  ● available")
                Text("both can run together").font(.caption2).foregroundStyle(.secondary)
            }.padding(10).background(.quaternary.opacity(0.18)).clipShape(RoundedRectangle(cornerRadius: 8))
            Text("💻 code  ○ idle"); Text("🧱 world  ○ idle")
            Text("🎨 assets  ○ idle"); Text("🎞 animation  ○ idle")
            Text("🔊 audio  ○ idle"); Text("🧪 testing  ○ idle"); Text("🔧 repair  ○ idle")
            Text("roblox studio").foregroundStyle(.secondary).bold().padding(.top, 18)
            Text("○ optional mcp bridge").foregroundStyle(.secondary)
            Button("configure mcp") {}
            Spacer()
        }.padding(16).frame(width: 290, alignment: .topLeading).background(.quaternary.opacity(0.15))
    }
}