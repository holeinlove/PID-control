# 迭代與驗收紀錄

本文件的一、二節保留原附件的需求歷史；其中的「原型通過」與使用者確認不代表本次正式 HTML 的驗收。三節起為 2026-10-13 新成品的實際測試紀錄。

## 一、已發生的需求迭代

下表根據本次實際對話整理，不是虛構的開發歷史。

| 階段 | 使用者回饋／需求 | AI 修改與設計決策 | 已有驗證／限制 |
|---|---|---|---|
| 需求釐清 | 用倒單擺教 PID，能調參並看控制波形 | 區分增益與 P/I/D 輸出；選用移動小車與末端重心 | 設計討論 |
| 控制目標修正 | 控制重心，允許左右移動，不要求回中央，先忽略重量 | 採速度指令 PID；不加小車位置控制；重心相對支點回授 | 確認方向與速度指令不是施力 |
| 第一版原型 | 一鍵平衡、重心在末端、能重設下垂 | 建立可操作對話內原型；獨立起擺再交給 PID；預設 6/12/1 | 直立偏 6°、下垂起擺、短暫干擾的 30 秒數值測試通過 |
| 干擾與教學 | 手動速度至少 3；下垂重設 PID 歸零；平衡時不要建議；加入圖文公式 | 上限提高 3；加入以時間窗判斷的回饋、P/I/D 圖解 | 數值測試、回饋分支、UI 回呼測試；不是完整瀏覽器視覺驗收 |
| 控制流程修正 | 不要開始鈕；重置全零下垂；重新開始保留參數；越界自動重跑 | 三按鈕、兩種初始姿態、本輪快照、越界清空動態並重跑 | 測試全零重置、保留参数、左右越界、兩種姿態、積分／波形／按鍵清除 |
| 使用者確認 | 「好，已符合我的結果」 | 將已確認原型整理成規格 | 使用者确认功能方向 |
| 評分與命名修正 | 依 9～10 分標準改善規格，可用 Markdown／圖片；HTML 指定檔名 | 建立本規格、UI SVG、驗收矩陣與紀錄；具名主檔＋同內容 index 入口 | 本次交付文件，不宣稱最終網站已部署 |

## 二、既有測試與新成品的界線

原型測試不能證明其他 AI 依規格生成的程式也正確。新成品需重新跑所有適用验收，尤其視覺、輸入、數值取樣、精確 2 秒判定與部署。規格補充了初版需要正式化的細節，不可直接把原型片段改副檔名就當完整交付。

已觀察到：強手動干擾後擺桿可能回到直立，但小車持續移動而越界。最終需求將此情況改為自動重跑；不是用位置控制消除漂移。

## 三、本次正式實作與測試環境

- 日期：2026-10-13（Asia/Taipei）。
- 正式主檔：`PID control Cart-Pole.html`。`index.html` 由主檔複製，未獨立維護。
- 本次工作目錄原為網路分享，但此環境無法存取；交付改存本次聊天本機可寫入目錄的 `pid-control/`。
- 瀏覽器：Chrome 155.0.8059.40（Windows）。Node.js v24.19.0、Playwright。沒有宣稱其他瀏覽器已測。
- 離線實測採 file: URL 與瀏覽器 offline 模式；不是只有檢查原始碼沒有外部連結。
- 總結：A01～A24 全部完成指定範圍驗收。23項本機驗收與A22部署後線上驗收分開記錄；Chrome以外瀏覽器、實體手機仍未宣稱測試。
- 本次原始規格第7節公式未更換。場景與圖表只讀模擬結果，正常控制流程不會直接修改角度來扶正擺桿。

## 四、本次迭代與真實修正

| 日期／版本 | 發現或需求 | 修改／處理 | 實際測試結果 |
|---|---|---|---|
| 2026-10-13 / 模型先行 | 必須先驗證速度 PID 與獨立起擺 | 寫純模型：半隱式 Euler、dt=1/240、條件積分、切換預置積分 | down/near 各30秒均穩定；下垂約2.270833秒切PID，不改控制常數 |
| 2026-10-13 / 正式單檔 | 介面必須可離線且資料真實 | 將已測模型原樣內嵌，加入狀態/表單/三按鈕/鍵盤/觸控/波形/圖文教學 | 從正式HTML再擷取模型驗證；不是引用原型通過紀錄 |
| 2026-10-13 / 版面與操作 | 320px可用、手動與控制輸出不可混淆 | 響應式堆疊、44px以上按鈕、示意比例、分列 raw/受限指令/實際車速 | 三尺寸DOM斷言與真實截圖通過；未以參考SVG當測試證據 |
| 2026-10-13 / 背景測試修正 | 首次用Page.setWebLifecycleState(frozen)未使頁面隱藏，模擬時間仍增長 | 調查工具預設Emulation.setFocusEmulationEnabled，改為獨立Chrome + noDefaults，實際切分頁 | 原測試失敗保留在browser-tests-initial.json；正式背景實測hidden=true時間不變，返回不追算 |
| 2026-10-13 / 測試工具啟動 | 獨立Chrome首度CDP連線逾時 | 增補隔離測試Chrome啟動旗標--no-sandbox/--disable-dev-shm-usage，未改HTML控制邏輯 | 背景測試可執行並通過；profile為測試獨立暫存 |
| 2026-10-13 / 證據製作 | 預設Python無Pillow | 使用Codex提供的Python依賴生成真實截圖序列GIF與裁切，未生成虛構畫面 | GIF來自45張實際瀏覽器畫面，讀值另存JSON；完整截圖仍保留 |
| 2026-10-13 / 完整回歸 | 加驗 near 30秒、真實多點touchCancel、重跑迴圈與長影格上限 | 擴充真實瀏覽器測試，重跑測試；未變更應用模型 | 最終瀏覽器測試全部通過；完整結果見browser-tests.json |
| 2026-10-13 / 錄製視窗修正 | 初次錄製視窗只涵蓋部分波形高度 | 將錄製視窗提高到1280px，依原比例製作GIF並單獨重跑干擾錄製 | 操作按鈕、模型與兩張波形可同時檢視；browser-recording-tests.json通過，實際畫面序列更新 |
| 2026-10-13 / 耐久與交付 | 5分鐘不能用加速模擬替代；部署不可未核准即執行 | 真實等待310秒，讀取陣列/RAF/錯誤；產生index及雜湊，上傳前僅唯讀查GitHub | 真實測試通過；GitHub預設main、空儲存庫、Pages未啟用；未push或發布 |

測試 fixture 說明：兩側邊界、下垂誤判、精確時間窗、受限／震盪回饋的部分測試會在測試程式中指定物理狀態或觀察樣本，以覆蓋特定條件。這些數值不是畫面假資料；正常應用沒有測試 fixture、預錄動畫或直接扶正操作。30秒穩定、全零失敗、310秒耐久與干擾GIF皆是實際積分／操作結果。

## 五、A01～A24 驗收矩陣

所有證據均位於 `evidence/`，唯本文件、上傳清單與測試說明除外。

| ID | 結果 | 操作與實際觀察 | 證據 |
|---|---|---|---|
| A01 | 通過 | 首次 file: 開啟，PID 0/0/0、V=3、下垂待機，t=0。 | initial-1280.png；browser-tests.json |
| A02 | 通過 | 實際點擊重置；PID/V 全零、下垂、x/v/ω/z/t/曲線/次數清空、停止。 | browser-tests.json |
| A03 | 通過 | UI 保留 7/13/1.2、V=1.4 並重跑兩次；純數值對相同初始條件逐位數值一致。 | browser-tests.json；numerical-tests.json |
| A04 | 通過 | 一鍵平衡套用 6/12/1，保留 V=1.7；另測 V=0 不被提高；僅三個主按鈕。 | browser-tests.json |
| A05 | 通過 | 下垂、無干擾，純數值與瀏覽器各跑滿 30 模擬秒；2.270833 s 切換 PID，無越界／失敗，最後穩定。 | numerical-tests.json；balanced-down-30s.png；browser-tests.json |
| A06 | 通過 | 直立偏 6° 直接 PID，純數值與瀏覽器各跑滿 30 模擬秒，無越界／失敗，最後穩定。 | numerical-tests.json；balanced-near-30s.png；browser-tests.json |
| A07 | 通過 | 鍵盤左右／雙按／放開斷言；320px 真實 CDP touchStart 雙點及 touchCancel；長按不累加。 | browser-tests.json；numerical-tests.json |
| A08 | 通過 | PID 階段 V=3，實際鍵盤起步、放開、換向，錄製 45 幀；偏移與波形改變，速度不超過 ±4。 | manual-disturbance.gif；disturbance-measurements.json；numerical-tests.json |
| A09 | 通過 | V=0 有就地提示且手動貢獻為 0；PID 仍移動小車，一鍵平衡保留 V=0。 | browser-tests.json；numerical-tests.json |
| A10 | 通過 | 左右邊界使用 x=±7.99999、v=±4 的明示測試 fixture 觸發真實一步積分；快照、資料、按鍵及次數均符合；長跑另自然重跑5次。 | browser-tests.json；numerical-tests.json；endurance-tests.json |
| A11 | 通過 | UI 啟動 near 後只改選單 down；邊界 fixture 仍以 near 重跑，手動重新開始才採 down。 | browser-tests.json |
| A12 | 通過 | 下垂 e≈0、y=-1 不判成功；額外測試短於完整2秒及当前角速度不符不得成功。 | numerical-tests.json |
| A13 | 通過 | 非預設 7/13/1.2 數值與 UI 均達穩定；回饋僅顯示已穩定，不要求換預設。 | nondefault-balanced.png；browser-tests.json；numerical-tests.json |
| A14 | 通過 | 起擺／手動中與剛放開／改參數不足2秒分支；另以明示回饋 fixture 檢查受限、震盪與無法唯一診斷。 | numerical-tests.json；browser-tests.json |
| A15 | 通過 | 全零 PID、near 初始，自然在約0.966667秒失衡；回饋說明無修正且不足完整2秒，不假稱時間窗完整。 | zero-gains-failure.png；numerical-tests.json；browser-tests.json |
| A16 | 通過 | 空白、非數字、NaN、Infinity、超界數值之驗證；UI 空白/超界阻止重跑並保留有效值；欄位內方向鍵不控制車。 | numerical-tests.json；browser-tests.json |
| A17 | 通過 | 逐筆比對 P=Kp·e、D=Kd·de、raw=manual+P+I+D；候選 I 與拒絕後 z 分開；30Hz、12秒、最多360筆。 | numerical-tests.json |
| A18 | 通過 | 角度自然超過1.05 rad停止，時間與曲線保持；修改／一鍵平衡可啟動新一輪。 | browser-tests.json；numerical-tests.json |
| A19 | 通過 | 實際滑鼠 capture／外部放開；真實觸控取消；blur；隔離瀏覽器實際背景切換；250ms長影格最多追算0.05s；20次重置／重跑仍單一RAF。 | browser-tests.json；visibility-tests.json（首次失敗測試另保留） |
| A20 | 通過 | 320/768/1280px 完整截图與 DOM 斷言均無水平溢出；所有按鈕高寬≥44px；逐圖檢視文字、圖解與操作。 | layout-320.png；layout-768.png；layout-1280.png；browser-tests.json |
| A21 | 通過 | Chrome context offline 下直接 file: 開啟／重新載入主檔，模擬、4幅內嵌SVG、教學可用；外部請求0，錯誤0。 | browser-tests.json；numerical-tests.json |
| A22 | 通過（線上） | 2026-10-13T16:01:34.025+08:00；Pages根網址及具名HTML均HTTP 200，首次待機、起擺→PID→穩定、全零重置、方向干擾皆通過；兩網址與本機HTML SHA-256一致。 | browser-tests.json的onlineAcceptance；hashes.json；線上截圖在本機交付ZIP |
| A23 | 通過 | 實際連續運行約310.36秒，5次自然重跑，取樣陣列上限360，待執行RAF始終1，控制台錯誤0。另有300模擬秒測試。 | endurance-tests.json；endurance-310s.png；numerical-tests.json |
| A24 | 通過（交付） | 36個核准路徑已上傳main；規格、應用、歷史與新驗收證據對應，核准／實際應用commit／公開網址已補齊；線上截圖另放本機交付包。 | 本文件；upload-manifest.json；Git提交紀錄 |

數值測試：20 個斷言案例全部通過。最終瀏覽器測試：18 組全部通過。耐久測試另立紀錄，真實經過 310.363 秒，非加速時鐘。

## 六、檔案與雜湊

- `PID control Cart-Pole.html`：正式應用，CSS／JavaScript／SVG全部內嵌。
- `index.html`：主檔逐位元複本，GitHub Pages入口。
- `PID-control-Cart-Pole-spec.md`：原規格原樣保留。
- `ui-reference.svg`：原配置參考原樣保留，應用不依賴它。
- `ITERATION-AND-ACCEPTANCE.md`：本文件，保留需求歷史與本次真實測試。
- `tests/`：可重跑數值、瀏覽器、真實耐久、背景切換及證據整理腳本與說明。
- `evidence/`：實際測試JSON、截圖與操作GIF。初次失敗測試也保留。
- `upload-manifest.json`：準備上傳的逐檔名、bytes、SHA-256與部署範圍；manifest本身也在核准範圍。
- 原始45張干擾PNG留在本機 `evidence/disturbance-frames/`；核准清單以GIF與量測JSON為準。

主檔與index的SHA-256（相同）：

`251b5596c2ec9cc678de38a12d476fa78572314d301c24148c22eaef42fdf52c`

## 七、已核准的GitHub上傳與發布紀錄

- 使用者明確核准訊息：「好，幫我發布」。核准紀錄時間：2026-10-13T15:56:58.314+08:00（Asia/Taipei；紀錄時間，非推定訊息發送时间）。
- 核准範圍：原清單36檔上傳main，啟用main根目錄GitHub Pages，完成線上驗收與交付紀錄。沒有新增Actions工作流程，未擴大遠端檔案清單。
- 發布帳號：holeinlove。官方Git Credential Manager登入成功，已確認對指定儲存庫具有push/admin權限；未將憑證写入成品或紀錄。
- 目標儲存庫：<https://github.com/holeinlove/PID-control>。
- 目標分支：main。上傳前唯讀檢查為空儲存庫且Pages未啟用；本次無覆蓋其他既有作品。
- 應用程式實際commit：`3878a3208001945f08af935d48281f593db097d6`（Build offline PID Cart-Pole teaching lab with verified tests）。
- 首次Pages部署：GitHub API status=built；build commit為上述應用commit；2026-10-13T07:59:03Z（臺灣15:59:03）完成，build error.message=null。
- Pages來源：main分支根目錄，legacy branch build。之後對該來源的push會自動重建發布。
- 公開根網址：<https://holeinlove.github.io/PID-control/>。
- 具名HTML網址：<https://holeinlove.github.io/PID-control/PID%20control%20Cart-Pole.html>。
- A22實測時間：2026-10-13T16:01:34.025+08:00；Chrome 155.0.8059.40。根網址1280px、具名網址320px均通過實際操作與無水平溢出檢查。
- 兩份線上HTML各38,599 bytes，SHA-256均為`251b5596c2ec9cc678de38a12d476fa78572314d301c24148c22eaef42fdf52c`，與已驗收本機主檔相同。上傳與發布沒有修改物理、控制模型或介面程式。
- 兩頁首次開啟均為PID=0、V=3、下垂待機；一鍵平衡實際起擺，在約5.35模擬秒觀察到穩定；重置全零待機；V=1的方向干擾造成真實速度與偏移變化。
- 兩頁應用JavaScript pageerror均0。根頁瀏覽器額外請求`https://holeinlove.github.io/favicon.ico`回404（已記錄實際資源URL）；這是瀏覽器預設網站圖示，應用不依賴它，不屬模擬／教學資源失敗。沒有把這條訊息偽記成不存在。
- 線上驗收結構化資料已補入原核准檔案`evidence/browser-tests.json`的`onlineAcceptance`。
- 真實線上截圖`evidence/online-root.png`與`evidence/online-named-320.png`保存於本機最終交付ZIP；為維持原核准36檔範圍，未新增這兩個遠端路徑。
- 本次後續提交僅補齊核准／部署／線上驗收紀錄與相應雜湊，HTML內容不變；文件提交的實際commit見Git歷史與最終交付訊息。

## 八、交付狀態與測試範圍

指定工作已完成：36檔上傳、Pages公開發布、A01～A24驗收及真實紀錄。沒有尚待核准的既定發布步驟。

本次測試範圍為Windows Chrome與320px觸控模擬；其他瀏覽器、實體手機未做相容性測試，不宣稱所有裝置通過。
