import Foundation
import SwiftUI

@main
struct AiroRobloxBuilderApp: App {
    var body: some Scene {
        WindowGroup("airobloxbuilder") { ContentView().frame(minWidth: 1050, minHeight: 680) }
    }
}

final class AIRuntime: ObservableObject {
    @Published var messages: [String] = ["airobloxbuilder: what are we building?"]
    private var process: Process?
    private var input: Pipe?

    func start() {
        let process = Process(), stdin = Pipe(), stdout = Pipe()
        let python = ProcessInfo.processInfo.environment["AIRO_PYTHON"] ?? "/usr/bin/python3"
        let runtimeDir = ProcessInfo.processInfo.environment["AIRO_RUNTIME_DIR"] ?? URL(fileURLWithPath: FileManager.default.currentDirectoryPath).appendingPathComponent("src/ai").path
        process.executableURL = URL(fileURLWithPath: python); process.arguments = ["-u", "-m", "runtime"]
        process.currentDirectoryURL = URL(fileURLWithPath: runtimeDir)
        var env = ProcessInfo.processInfo.environment; env["PYTHONPATH"] = runtimeDir; process.environment = env
        process.standardInput = stdin; process.standardOutput = stdout; process.standardError = stdout
        stdout.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData; guard !data.isEmpty, let text = String(data: data, encoding: .utf8) else { return }
            DispatchQueue.main.async { text.split(whereSeparator: \.isNewline).forEach { self?.handle(String($0)) } }
        }
        do { try process.run(); self.process = process; self.input = stdin } catch { messages.append("runtime: \(error.localizedDescription)") }
    }

    func send(_ text: String) {
        guard let input, process?.isRunning == true else { messages.append("runtime: ai runtime is not running."); return }
        let projectRoot = ProcessInfo.processInfo.environment["AIRO_PROJECT_ROOT"] ?? FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0].appendingPathComponent("airobloxbuilder/projects/my game").path
        try? FileManager.default.createDirectory(atPath: projectRoot, withIntermediateDirectories: true)
        let request: [String:String] = ["request_id": UUID().uuidString, "text": text, "project_root": projectRoot]
        guard let data = try? JSONSerialization.data(withJSONObject: request) else { return }
        input.fileHandleForWriting.write(data); input.fileHandleForWriting.write(Data([10]))
    }

    private func handle(_ line: String) {
        guard let data = line.data(using: .utf8), let object = try? JSONSerialization.jsonObject(with: data) as? [String:Any],
              let type = object["type"] as? String else { return }
        let message = object["message"] as? String ?? ""
        if type == "progress" { messages.append("🧠 \(message)  •  ● ● ●") }
        else if type == "route" { messages.append("✨ \(message)  •  working") }
        else if type == "text" { messages.append("airobloxbuilder: \(message)") }
        else if type == "error" { messages.append("runtime: \(message)") }
        else if type == "complete" { messages.append("✨ ✓ finished") }
    }
    deinit { process?.terminate() }
}

struct ContentView: View {
    @StateObject private var runtime = AIRuntime()
    @State private var prompt = ""
    @State private var extras = false
    var body: some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                Button("☰") { extras.toggle() }.buttonStyle(.bordered)
                Text("◈").font(.title2).foregroundStyle(.purple); Text("my zombie mall").font(.title2.weight(.semibold))
                Spacer(); Text("● online").foregroundStyle(.green); Text("macos").foregroundStyle(.secondary)
            }.padding(.horizontal, 22).frame(height: 72)
            Divider()
            HStack(spacing: 0) {
                ProjectPane(); Divider()
                VStack {
                    ScrollViewReader { proxy in
                        ScrollView { LazyVStack(alignment: .leading, spacing: 14) {
                            ForEach(Array(runtime.messages.enumerated()), id: \.offset) { _, message in
                                Text(message).frame(maxWidth: .infinity, alignment: .leading).padding(.vertical, 3)
                            }
                        }.frame(maxWidth: 940).padding(24).onChange(of: runtime.messages.count) { proxy.scrollTo(runtime.messages.count - 1) }
                    }
                    HStack { TextField("tell airo what to build...", text: $prompt).textFieldStyle(.roundedBorder).onSubmit(send); Button("➤", action: send).buttonStyle(.borderedProminent) }.frame(maxWidth: 940).padding(.horizontal,24).padding(.bottom,22)
                }
            }
            Divider()
            HStack { Text("free forever • native • build anywhere").foregroundStyle(.secondary); Spacer(); Text("ai runtime connected").foregroundStyle(.secondary) }.padding(.horizontal,22).frame(height:78)
        }
        .overlay(alignment: .topLeading) {
            if extras { ExtrasMenu().padding(.top, 62).padding(.leading, 22) }
        }
    }
    private func send() { let value=prompt.trimmingCharacters(in:.whitespacesAndNewlines); guard !value.isEmpty else{return}; runtime.messages.append("you: \(value)"); runtime.send(value); prompt="" }
}

struct ProjectPane: View {
    var body: some View {
        VStack(alignment:.leading,spacing:9) {
            Text("project").foregroundStyle(.secondary).bold()
            Text("📁 my game").font(.headline).padding(.top,14)
            Text("📜  scripts"); Text("🌎  worlds"); Text("🧱  assets"); Text("🎵  audio"); Text("🎨  ui"); Text("🧪  tests")
            RoundedRectangle(cornerRadius:14).fill(.quaternary.opacity(0.25)).frame(height:76).overlay(alignment:.topLeading) { VStack(alignment:.leading){Text("tasks").foregroundStyle(.secondary).bold();Text("○ waiting for work").foregroundStyle(.secondary).font(.caption)}.padding(13) }.padding(.top,22)
            Text("tip").foregroundStyle(.secondary).bold().padding(.top,16)
            Text("describe the game naturally. airo keeps project context between requests.").font(.caption).foregroundStyle(.secondary)
            Spacer()
        }.padding(22).frame(width:250).background(.quaternary.opacity(0.08))
    }
}

struct ExtrasMenu: View {
    var body: some View {
        VStack(alignment:.leading,spacing:6) {
            Text("extras").font(.headline).padding(8)
            ForEach(["📁  projects","📋  tasks","🐙  github","🔌  roblox studio","🧠  model","📦  import / export","⚙  settings"],id:\.self) { item in Button(item) {}.buttonStyle(.plain).padding(9).frame(maxWidth:.infinity,alignment:.leading) }
        }.padding(8).frame(width:245).background(.regularMaterial).clipShape(RoundedRectangle(cornerRadius:16)).shadow(radius:18)
    }
}