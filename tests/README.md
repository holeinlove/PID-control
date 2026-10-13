# 測試與證據重現

主檔是唯一維護來源。數值測試直接從 `PID control Cart-Pole.html` 擷取 `physics-model`，沒有另外維護的模擬器。HTML 本身不需要任何測試套件。

本次環境：Windows、Node.js v24.19.0、Playwright、Chrome 155.0.8059.40；2026-10-13（Asia/Taipei）。

在交付根目錄執行：

```powershell
node tests/numerical.cjs
node tests/browser.cjs
node tests/endurance.cjs
node tests/visibility.cjs
python tests/make-evidence.py
```

- 瀏覽器腳本需要 `playwright` 可由 Node 解析（本次使用 Codex 內建套件並設定 NODE_PATH），以及 `C:\Program Files\Google\Chrome\Application\chrome.exe`。其他環境請將執行檔路徑／channel 改為實際安裝位置。
- `browser.cjs` 約需 90 秒；`endurance.cjs` 真實等待 310 秒。兩者使用 `file:` 開啟主檔，瀏覽器 context 設為 offline。
- `visibility.cjs` 為避免 Playwright 預設 focus emulation 將背景分頁視為前景，另啟動隔離 Chrome，以 `connectOverCDP(..., {noDefaults:true})` 連線，實際切換分頁。不覆寫 document.hidden。
- `make-evidence.py` 需要 Pillow；它將真實瀏覽器截圖序列製成 GIF、產生窄螢幕檢視裁切。原始完整截圖仍保留。錄製是取樣畫面序列，擷取速度受機器影響；狀態與模擬時間另存在 disturbance-measurements.json。
- 左右邊界與少數回饋分支以**明確標示的測試 fixture**設定數值，驗證邊界／判斷條件。正常 HTML 的控制器沒有這些測試注入，也沒有直接扶正角度。
- 修改主檔後先複製成 `index.html`，再重新測試。不要獨立修改 index。任何來源變更均需更新雜湊與 upload-manifest.json。
- 首輪錯誤測試保留於 `evidence/browser-tests-initial.json`；修正測試方式後的最終結果為 `evidence/browser-tests.json`，背景實測另見 visibility-tests.json。
- 執行 browser.cjs 會在 evidence/disturbance-frames 產生逐幀 PNG；上傳清單採 GIF 與量測 JSON，逐幀 PNG 留於本機。

使用者已於2026-10-13明確核准發布，A22線上驗收已完成。結果見 evidence/browser-tests.json 的 onlineAcceptance 與 ITERATION-AND-ACCEPTANCE.md。package-review.py 為核准前封裝腳本的歷史版本；最終發布交付包另名為 PID-control-published.zip。
