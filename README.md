# 操作參考 SOP

1. 安裝 python 相關模組
pip install -r requirements.txt

2. 創建 .env 檔案進行相關設定
- start_img: 輸入 laplace 後的檔名，系統會從這張圖片的下一張開始處理
Ex: start_img="lap_1716290708-wwsd.png"
- counter_start: 用來設定這批裁切箭頭的輸出照片開頭編號
Ex: counter_start=100，則這次被處理的圖片第一張第一個箭頭會是編號100
- debug: 除錯模式，當設定為True時會顯示這批裁減箭頭的繪圖，同時不會儲存裁切結果
Ex: debug=True

3. 執行前處理指令 pyhton -m preprocessing.preprocessor
- 標註: 對 raw 底下未被標註的照片進行人工標注，標注後檔名會加上標注結果
- laplace: 對 raw 底下所有照片進行拉普拉斯轉換，儲存結果，檔名前綴 lap_
- 篩選: 利用 start_img 設定，決定要裁切的 laplace 開始圖片
- 裁切: 讀取 laplace 結果、定位箭頭位置，最後依 debug 設定決定要顯示或儲存。儲存的結果會由 counter_start 作為起始編號儲存在 cut 相關目錄底下。
- 標準化: 讀取 cut 目錄下裁切箭頭，將其大小拉伸到 32 x 32 x 3
- (TODO) 訓練資料準備: 實作一程式，顯示被拉伸後的箭頭，接收使用者輸入來決定是否使用這張圖片。如果使用，要在這裡進行 augmentation 增加資料量。並將結果儲存到 train 目錄底下
(也就是說使用者應該在這步驟篩選資料，而非刪除 raw_data)

4. 深度學習