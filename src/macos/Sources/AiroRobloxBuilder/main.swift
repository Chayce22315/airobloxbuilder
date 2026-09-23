import SwiftUI

@main
struct AiroRobloxBuilderApp: App {
    var body: some Scene {
        WindowGroup("airobloxbuilder") {
            ContentView()
                .frame(minWidth: 960, minHeight: 600)
        }
    }
}

struct ContentView: View {
    @State private var prompt = ""
    @State private var messages = ["builder: what are we building?"]

    var body: some View {
        HStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 10) {
                Text("◈ airobloxbuilder")
                    .font(.title2.weight(.semibold))
                Text("project")
                    .font(.headline)
                    .padding(.top, 22)
                Text("📁 my game")
                Text("  ├─ scripts")
                Text("  ├─ assets")
                Text("  ├─ maps")
                Text("  ├─ audio")
                Text("  └─ ui")
                Spacer()
            }
            .padding(18)
            .frame(width: 250)

            VStack {
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 14) {
                        ForEach(messages, id: \.self) { message in
                            Text(message)
                                .frame(maxWidth: .infinity, alignment: .leading)
                        }
                    }
                }

                HStack {
                    TextField("describe your game or tell the builder what to do...", text: $prompt)
                        .textFieldStyle(.roundedBorder)
                    Button("➤") {
                        send()
                    }
                }
            }
            .padding(18)

            VStack(alignment: .leading, spacing: 12) {
                Text("🧠 agents")
                    .font(.title2.weight(.semibold))
                Text("orchestrator  ○ idle")
                Text("💻 code  ○ idle")
                Text("🧱 world  ○ idle")
                Text("🎨 assets  ○ idle")
                Text("🧪 testing  ○ idle")
                Text("🔧 repair  ○ idle")
                Spacer()
            }
            .padding(18)
            .frame(width: 280)
        }
    }

    private func send() {
        let value = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !value.isEmpty else { return }
        messages.append("you: \(value)")
        messages.append("builder: request received. the orchestrator is not connected yet, but the native shell is alive.")
        prompt = ""
    }
}
