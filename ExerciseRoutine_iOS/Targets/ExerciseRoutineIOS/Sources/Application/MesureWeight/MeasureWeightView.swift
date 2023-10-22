//
//  NumberButtonView.swift
//  ExerciseRoutineIOS
//
//  Created by Doy Kim on 2023/10/22.
//  Copyright © 2023 com.kimdee. All rights reserved.
//
//  참고: youtu.be/fRIYwYangAA

import SwiftUI

struct MeasureWeightView: View {
    @State var value = "0"
    @State var numberShowing = 0
    @State var currentOperation: CalculatorOperation = .none
    
    let buttons: [[CalculatorButton]] = [
        [.clear],
        [.seven, .eight, .nine],
        [.four, .five, .six],
        [.one, .two, .three],
        [.dot, .zero, .delete]
    ]
    private let spacing: CGFloat = 16
    
    var body: some View {
        VStack {
            Text(value)
                .font(.system(size: 96))
            ForEach(buttons, id: \.self) { row in
                HStack(spacing: spacing) {
                    ForEach(row, id: \.self) { item in
                        Button {
                            self.didTap(button: item)
                        } label: {
                            Text(item.rawValue)
                                .font(.system(size: 32))
                                .foregroundColor(item.buttonColor)
                                .frame(width: getButtonWidth(button: item),
                                       height: getButtonHeight())
                                .background(item.buttonBGColor)
                                .clipShape(RoundedRectangle(cornerRadius: 12))
                        }
                    }
                }
            }
        }
    }
    
    func didTap(button: CalculatorButton) {
        switch button {
        case .clear:
            self.value = "0"
            self.numberShowing = 0
            self.currentOperation = .clear
        case .delete:
            if self.value.count > 1 {
                self.value = String(self.value.dropLast())
            } else {
                self.value = "0"
            }
        default:
            if self.value == "0" {
                self.value = button.rawValue
            } else {
                self.value = "\(self.value)\(button.rawValue)"
            }
        }
    }
    
    func getButtonWidth(button: CalculatorButton) -> CGFloat {
        if button == .clear {
            return ((UIScreen.main.bounds.width - (spacing*2)))
        } else {
            return ((UIScreen.main.bounds.width) - (spacing*4))/3
        }
    }
    func getButtonHeight() -> CGFloat {
        return (UIScreen.main.bounds.width)/5
    }
}

struct MeasureWeightView_Previews: PreviewProvider {
    static var previews: some View {
        MeasureWeightView()
    }
}
