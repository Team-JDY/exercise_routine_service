//
//  Color+.swift
//  ExerciseRoutineIOS
//
//  Created by Doy Kim on 2023/10/22.
//  Copyright © 2023 com.kimdee. All rights reserved.
//

import SwiftUI

/// 헥사값으로 색상을 사용할 수 있는 메서드 추가
/// 참고: stackoverflow.com/questions/56874133/use-hex-color-in-swiftui
extension Color {
    init(hex: Int, opacity: Double = 1.0) {
        let red = Double((hex & 0xff0000) >> 16) / 255.0
        let green = Double((hex & 0xff00) >> 8) / 255.0
        let blue = Double((hex & 0xff) >> 0) / 255.0
        self.init(.sRGB, red: red, green: green, blue: blue, opacity: opacity)
    }
}
