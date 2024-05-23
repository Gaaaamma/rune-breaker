from os import listdir
import tkinter as tk
from tkinter import PhotoImage
from setting import SETTINGS

class ImageSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display and Key Press Monitor")
        
        # 圖片檔案清單
        self.image_files = sorted(listdir(SETTINGS.standard_data_dir))
        self.answer_files = ["w.png", "s.png", "a.png", "d.png"]
        self.ans_map = {'w': 0, "s": 1, "a": 2, "d": 3}

        # 當前顯示的圖片索引
        self.current_image_index = 0
        
        # 載入圖片
        self.images = [PhotoImage(file=f"{SETTINGS.standard_data_dir}{img}") for img in self.image_files]
        self.answer = [PhotoImage(file=f"{SETTINGS.answer_data_dir}{img}") for img in self.answer_files]

        # 創建畫布來顯示圖片
        self.canvas1 = tk.Canvas(root, width=self.images[0].width(), height=self.images[0].height())
        self.canvas1.pack(side=tk.LEFT)
        self.image_id1 = self.canvas1.create_image(0, 0, anchor=tk.NW, image=self.images[self.current_image_index])
        img_name: str = self.image_files[self.current_image_index]
        print(img_name)

        ans_img_index = self.ans_map[img_name.split("-")[-1].split(".")[0]]
        self.canvas2 = tk.Canvas(root, width=self.answer[0].width(), height=self.answer[0].height())
        self.canvas2.pack(side=tk.LEFT)
        self.image_id2 = self.canvas2.create_image(0, 0, anchor=tk.NW, image=self.answer[ans_img_index])
        
        # 綁定鍵盤事件
        self.root.bind('<KeyPress>', self.on_key_press)
        
    def on_key_press(self, event):
        if event.char == 'y':
            print("yes")
            self.switch_image()
        else:
            print("no")
    
    def switch_image(self):
        # 切換圖片索引
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        img_name: str = self.image_files[self.current_image_index]
        print(img_name)
        ans_img_index = self.ans_map[img_name.split("-")[-1].split(".")[0]]

        # 更新畫布中的圖片
        self.canvas1.itemconfig(self.image_id1, image=self.images[self.current_image_index])
        self.canvas2.itemconfig(self.image_id2, image=self.answer[ans_img_index])

def main():
    root = tk.Tk()
    app = ImageSwitcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()