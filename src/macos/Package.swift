// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "AiroRobloxBuilder",
    platforms: [.macOS(.v14)],
    products: [
        .executable(name: "airobloxbuilder", targets: ["AiroRobloxBuilder"])
    ],
    targets: [
        .executableTarget(name: "AiroRobloxBuilder")
    ]
)
