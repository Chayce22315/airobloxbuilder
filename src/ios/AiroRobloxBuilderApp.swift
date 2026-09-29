import SwiftUI
import Foundation
import UIKit

@main
struct AiroRobloxBuilderApp: App {
    var body: some Scene {
        WindowGroup { PhoneRootView() }
    }
}

struct PhoneRootView: View {
    @State private var projectName = "my zombie mall"
    @State private var prompt = ""
    @State private var messages: [ChatItem] = [
        ChatItem(speaker: "airobloxbuilder", text: "what are we building?", kind: .builder)
    ]
    @State private var extras = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                HStack(spacing: 10) {
                    Button { extras = true } label: { Image(systemName: "line.3.horizontal").font(.title3.weight(.semibold)).frame(width: 38,height:38) }
                        .buttonStyle(.plain)
                    Text("◈").font(.title2).foregroundStyle(.purple)
                    Text(projectName).font(.headline.weight(.semibold)).lineLimit(1)
                    Spacer()
                    Circle().fill(.green).frame(width: 8,height: 8)
                }
                .padding(.horizontal, 16).frame(height: 58)

                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 16) {
                            ForEach(messages) { item in
                                ChatBubble(item: item).id(item.id)
                            }
                        }.padding(18)
                    }
                    .onChange(of: messages.count) { _, _ in
                        if let last = messages.last { withAnimation { proxy.scrollTo(last.id, anchor: .bottom) } }
                    }
                }

                HStack(spacing: 8) {
                    Button { } label: { Image(systemName: "plus").font(.headline).frame(width: 38,height: 38) }.buttonStyle(.plain)
                    TextField("tell airo what to do...", text: $prompt, axis: .vertical)
                        .lineLimit(1...4).padding(.horizontal,12).padding(.vertical,9)
                        .background(Color(uiColor: .secondarySystemBackground)).clipShape(RoundedRectangle(cornerRadius:14))
                    Button { send() } label: { Image(systemName: "arrow.up").font(.headline).frame(width: 38,height:38) }
                        .buttonStyle(.borderedProminent).tint(.purple)
                }.padding(12)
            }
            .background(Color(uiColor: .systemBackground))
            .sheet(isPresented: $extras) { ExtrasSheet(projectName: projectName) }
        }
    }

    private func send() {
        let value = prompt.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !value.isEmpty else { return }
        messages.append(ChatItem(speaker: "you", text: value, kind: .user))
        prompt = ""
        messages.append(ChatItem(speaker: "airobloxbuilder", text: "🧠 planning your project...  •  ● ● ●", kind: .thinking))
        ProjectStore().ensureProject(named: projectName)
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.45) {
            messages.append(ChatItem(speaker: "airobloxbuilder", text: "✨ local project builder is ready. generated changes will be written into the project structure.", kind: .builder))
        }
    }
}

final class ProjectStore {
    private let fileManager = FileManager.default

    func ensureProject(named name: String) {
        guard let documents = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first else { return }
        let root = documents.appendingPathComponent("airobloxbuilder/projects/\(safeName(name))", isDirectory: true)
        let directories = [
            "src/ServerScriptService",
            "src/ReplicatedStorage/Shared",
            "src/ReplicatedStorage/Remotes",
            "src/StarterPlayer/StarterPlayerScripts",
            "src/StarterGui",
            "src/Workspace",
            "src/ServerStorage",
            "assets/models",
            "assets/textures",
            "assets/animations",
            "assets/audio",
            "tests"
        ]
        for directory in directories {
            try? fileManager.createDirectory(at: root.appendingPathComponent(directory), withIntermediateDirectories: true)
        }
        let starter: [(String,String)] = [
            ("src/ServerScriptService/GameManager.server.luau", "-- airobloxbuilder starter\nlocal GameManager = {}\nreturn GameManager\n"),
            ("src/ReplicatedStorage/Shared/Config.luau", "return {\n    RoundLength = 300,\n    MaxPlayers = 12,\n}\n"),
            ("src/StarterPlayer/StarterPlayerScripts/Client.client.luau", "-- client entry point\n"),
            ("tests/GameManager.test.luau", "-- generated test entry point\n")
        ]
        for (path, contents) in starter {
            let url = root.appendingPathComponent(path)
            if !fileManager.fileExists(atPath: url.path) {
                try? contents.write(to: url, atomically: true, encoding: .utf8)
            }
        }
    }

    private func safeName(_ value: String) -> String {
        value.replacingOccurrences(of: "/", with: "-").replacingOccurrences(of: ":", with: "-")
    }
}

struct ChatItem: Identifiable {
    enum Kind { case user, builder, thinking }
    let id = UUID()
    let speaker: String
    let text: String
    let kind: Kind
}

struct ChatBubble: View {
    let item: ChatItem
    var body: some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(item.speaker).font(.subheadline.weight(.semibold)).foregroundStyle(item.kind == .user ? .blue : .green)
            if item.kind == .thinking {
                Text(item.text).font(.subheadline.weight(.semibold)).foregroundStyle(.purple)
                    .padding(13).background(.purple.opacity(0.09)).clipShape(RoundedRectangle(cornerRadius:14))
            } else {
                Text(item.text).font(.body).textSelection(.enabled)
            }
        }
    }
}

struct ExtrasSheet: View {
    let projectName: String
    @Environment(\.dismiss) private var dismiss
    var body: some View {
        NavigationStack {
            List {
                Section("extras") {
                    NavigationLink("📁  projects") { ProjectBrowser(projectName: projectName) }
                    NavigationLink("📋  tasks") { SimplePage(title: "tasks", subtitle: "your generated work plan will appear here.") }
                    NavigationLink("🐙  github") { SimplePage(title: "github", subtitle: "connect a repository and review pull requests.") }
                    NavigationLink("🔌  roblox studio") { SimplePage(title: "roblox studio", subtitle: "studio is unavailable on iphone, so this stays a project-only workflow.") }
                    NavigationLink("🧠  model") { SimplePage(title: "model", subtitle: "choose the model endpoint used by the builder.") }
                    NavigationLink("📦  import / export") { SimplePage(title: "import / export", subtitle: "move project files between devices and repositories.") }
                    NavigationLink("⚙️  settings") { SimplePage(title: "settings", subtitle: "configure the builder.") }
                }
            }.navigationTitle("extras").toolbar { ToolbarItem(placement: .topBarTrailing) { Button("done") { dismiss() } } }
        }
    }
}

struct ProjectBrowser: View {
    let projectName: String
    var body: some View {
        List {
            Section(projectName) {
                NavigationLink("📜  scripts") { FileList(title: "scripts", files: ["RoundSystem.server.luau","ZombieManager.server.luau","GameManager.server.luau"]) }
                NavigationLink("🌎  worlds") { FileList(title: "worlds", files: ["Mall.map.json"]) }
                NavigationLink("🧱  assets") { FileList(title: "assets", files: ["models/","textures/","animations/"]) }
                NavigationLink("🎵  audio") { FileList(title: "audio", files: ["music/","sfx/"]) }
                NavigationLink("🎨  ui") { FileList(title: "ui", files: ["MainGui.luau"]) }
                NavigationLink("🧪  tests") { FileList(title: "tests", files: ["RoundSystem.test.luau"]) }
            }
        }.navigationTitle("project")
    }
}

struct FileList: View {
    let title: String
    let files: [String]
    var body: some View { List(files, id: \.self) { Text($0).font(.body.monospaced()) }.navigationTitle(title) }
}

struct SimplePage: View {
    let title: String
    let subtitle: String
    var body: some View { VStack(alignment:.leading,spacing:12){ Text(title).font(.largeTitle.bold()); Text(subtitle).foregroundStyle(.secondary); Spacer() }.padding().navigationTitle(title) }
}