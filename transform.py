"""               
HID AbsoluteMouse coordination 
(-32767, -32767) ------------- # ------------- (32767, -32767) (1919, -1079)
                 |             |             |
                 |             |             |
                 |------------ 0 ------------| (32767, 0) 
                 |             |             |
                 |             |             |
(-32767, 32767)  ------------- # ------------- (32767, 32767) (1919, 1079)
"""

windows_width: int = 1920
windows_height: int = 1080
x_ratio: float = 34.133
y_ratio: float = 60.68

while True:
    print("Input (x, y)")
    x: int = int(input("x: "))
    y: int = int(input("y: "))
    
    result_x: int = x * x_ratio - 32767
    result_y: int = y * y_ratio - 32767
    print(f"Leonardo (x, y) = ({result_x}, {result_y})\n")