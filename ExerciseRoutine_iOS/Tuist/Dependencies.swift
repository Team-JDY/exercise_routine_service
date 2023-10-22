//
//  Dependencies.swift
//  Config
//
//  Created by Doy Kim on 2023/10/22.
//

import ProjectDescription

public let dependencies = Dependencies(
    swiftPackageManager: [
        .remote(url: "https://github.com/pointfreeco/swift-composable-architecture", requirement: .upToNextMinor(from: "1.2.0")),
        .remote(url: "https://github.com/Moya/Moya.git", requirement: .upToNextMinor(from: "15.0.0"))
    ],
    platforms: [.iOS]
)
