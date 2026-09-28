import Foundation
import SwiftUI

@main
struct AiroRobloxBuilderApp: App {
    var body: some Scene {
        WindowGroup("airobloxbuilder") { ContentView().frame(minWidth: 1050, minHeight: 680) }
    }
}

final class AIRuntime: ObservableObject {
    @Published var messages: [String] = ["builder: what are we building?"]
    private var process: Process?
    private var input: Pipe?

    func start() {
        let process = Process()
        let stdin = Pipe()
        let stdout = Pipe()
        let python = ProcessInfo.processInfo.environment["AIRO_PYTHON"] ?? "/usr/bin/python3"
        let runtimeDir = ProcessInfo.processInfo.environment["AIRO_RUNTIME_DIR"] ?? URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent("src/ai").path
        process.executableURL = URL(fileURLWithPath: python)
        process.arguments = ["-u", "-m", "runtime"]
        process.currentDirectoryURL = URL(fileURLWithPath: runtimeDir)
        var env = ProcessInfo.processInfo.environment
        env["PYTHONPATH"] = runtimeDir
        process.environment = env
        process.standardInput = stdin
        process.standardOutput = stdout
        process.standardError = stdout
        stdout.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty, let text = String(data: data, encoding: .utf8) else { return }
            let lines = text.split(whereSeparator: \.isNewline)
            DispatchQueue.main.async {
                for line in lines { self?.handle(String(line)) }
            }
        }
        do {
            try process.run()
            self.process = process
            self.input = stdin
            messages.append("runtime: ai runtime started. configure AIRO_API_URL and AIRO_MODEL to connect a real model.")
        } catch {
            messages.append("runtime: could not start ai runtime: \(error.localizedDescription)")
        }
    }

    func send(_ text: String) {
        guard let input, process?.isRunning == true else {
            messages.append("runtime: ai runtime is not running.")
            return
        }
        let request: [String: String] = ["request_id": UUID().uuidString, "text": text]
        guard let data = try? JSONSerialization.data(withJSONObject: request) else { return }
        input.fileHandleForWriting.write(data)
        input.fileHandleForWriting.write(Data([10]))
    }

    private func handle(_ line: String) {
        guard let data = line.data(using: .utf8), let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any], let type = object["type"] as? String else { return }
        if ["text", "error", "complete"].contains(type), let message = object["message"] as? String {
            messages.append("\(type == "error" ? "runtime" : "builder"): \(message)")
        }
    }

    deinit {
        process?.terminate()
    }
}

struct ContentView: View {
    @StateObject private var runtime = AIRuntime()
    @State private var prompt = ""

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                HStack(spacing: 10) { Text("◈ airobloxbuilder").font(.title2.weight(.semibold)); Text("native").font(.caption).padding(.horizontal,8).padding(.vertical,4).background(.green.opacity(0.12)).clipShape(Capsule()) }
                Spacer(); Text("● ai runtime").foregroundStyle(.green)
            }.padding(.horizontal, 18).frame(height: 54)
            Divider()
            HStack(spacing: 0) {
                ProjectPane(); Divider(); ChatPane(messages: $runtime.messages, prompt: $prompt, send: send); Divider(); AgentPane()
            }
            Divider()
            HStack { Text("free forever • native • windows first").foregroundStyle(.secondary); Spacer(); Text("v0.1 ai runtime").foregroundStyle(.secondary) }.padding(.horizontal, 18).frame(height: 62)
        }.onAppear { runtime.start() }
    }

    private func send() {
        let value = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !value.isEmpty else { return }
        runtime.messages.append("you: \(value)")
        runtime.send(value)
        prompt = ""
    }
}

struct ProjectPane: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("project").foregroundStyle(.secondary).bold(); Text("📁 my game").bold().padding(.top, 14)
            Text("  ├─ scripts"); Text("  ├─ assets"); Text("  ├─ maps"); Text("  ├─ audio"); Text("  ├─ ui"); Text("  └─ tests")
            Text("tasks").foregroundStyle(.secondary).bold().padding(.top, 20); Text("○ waiting for orchestrator").foregroundStyle(.secondary)
            Text("commands").foregroundStyle(.secondary).bold().padding(.top, 20); Text("/plan  /tasks  /test  /fix").font(.caption).foregroundStyle(.secondary)
            Spacer()
        }.padding(16).frame(width: 255, alignment: .topLeading).background(.quaternary.opacity(0.15))
    }
}

struct ChatPane: View {
    @Binding var messages: [String]
    @Binding var prompt: String
    let send: () -> Void
    var body: some View {
        VStack {
            ScrollView { LazyVStack(alignment: .leading, spacing: 14) { ForEach(Array(messages.enumerated()), id: \.offset) { _, message in Text(message).frame(maxWidth: .infinity, alignment: .leading) } } }
            HStack { TextField("describe your game or tell the builder what to do...", text: $prompt).textFieldStyle(.roundedBorder).onSubmit(send); Button("➤", action: send) }
        }.padding(18)
    }
}

struct AgentPane: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("🧠 agents").font(.title2.weight(.semibold)); Text("orchestrator  ● ready").padding(.top, 12)
            VStack(alignment: .leading, spacing: 6) { Text("live work").font(.caption.bold()).foregroundStyle(.secondary); Text("💬 chat  ● available"); Text("💻 code  ● available"); Text("both can run together").font(.caption2).foregroundStyle(.secondary) }.padding(10).background(.quaternary.opacity(0.18)).clipShape(RoundedRectangle(cornerRadius: 8))
            Text("💻 code  ○ idle"); Text("🧱 world  ○ idle"); Text("🎨 assets  ○ idle"); Text("🎞 animation  ○ idle"); Text("🔊 audio  ○ idle"); Text("🧪 testing  ○ idle"); Text("🔧 repair  ○ idle")
            Text("roblox studio").foregroundStyle(.secondary).bold().padding(.top, 18); Text("○ optional mcp bridge").foregroundStyle(.secondary); Button("configure mcp") {}
            Spacer()
        }.padding(16).frame(width: 290, alignment: .topLeading).background(.quaternary.opacity(0.15))
    }
}
