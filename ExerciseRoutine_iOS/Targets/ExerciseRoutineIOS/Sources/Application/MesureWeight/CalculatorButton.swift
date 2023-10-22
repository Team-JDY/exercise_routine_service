//
//  CalculatorButton.swift
//  ExerciseRoutineIOS
//
//  Created by Doy Kim on 2023/10/22.
//  Copyright © 2023 com.kimdee. All rights reserved.
//

import SwiftUI

enum CalculatorButton: String {
    case zero = "0"
    case one = "1"
    case two = "2"
    case three = "3"
    case four = "4"
    case five = "5"
    case six = "6"
    case seven = "7"
    case eight = "8"
    case nine = "9"
    case clear = "Clear"
    case dot = "."
    case delete = "⌫"
    
    var buttonColor: Color {
        switch self {
        default:
            return .white
        }
    }
    var buttonBGColor: Color {
        switch self {
        case .clear:
            return Color(hex: 0x4E505F)
        default:
            return Color(hex: 0x2E2F38)
        }
    }
}

enum CalculatorOperation {
    case delete, clear, dot, none
}
