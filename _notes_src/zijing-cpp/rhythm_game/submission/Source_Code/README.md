# aeacrA - README

## 版权声明 / Copyright Notice

本作品为课程项目，仅供学习交流使用，不用于任何商业用途。
This project is a course assignment, intended for learning purposes only, not for commercial use.

游戏玩法灵感来源于各类音乐节奏游戏（如 osu!mania、DJMAX 等）。
Gameplay inspiration comes from various rhythm games (e.g., osu!mania, DJMAX).

游戏内预置的歌曲仅供学习展示用途，版权属于原作者。
Pre-loaded songs are for demonstration purposes only; copyrights belong to their respective owners.

---

## 运行环境 / Environment

- macOS 12.0（Monterey）或更高版本 / macOS 12.0 (Monterey) or later
- Clang++ 编译器（支持 C++17）/ Clang++ compiler with C++17 support
- raylib 库（`brew install raylib`）/ raylib library
- aubio 库（`brew install aubio`）/ aubio library

---

## 编译与运行 / Build & Run

1. 打开终端，cd 到项目根目录（包含 Makefile 的目录）
   Open terminal, cd to the project root (where Makefile is located)
2. 执行 `make` / Run `make`
3. 运行 `./aeacrA` / Run `./aeacrA`

---

## 注意事项 / Notes

- 必须从项目根目录运行，否则 songs/ 和 charts/ 文件夹找不到
  Must run from project root, otherwise songs/ and charts/ directories won't be found
- 确保 songs/ 和 charts/ 文件夹存在（项目中已包含）
  Ensure songs/ and charts/ directories exist (included in the project)
- 导入歌曲时需要 macOS 文件访问权限，首次弹出系统对话框请点击允许
  macOS file access permission is required when importing songs; allow it when the system dialog appears

---

## 测试用例说明 / Test Cases

以下功能已通过手动测试验证：
The following features have been verified through manual testing:

| # | 测试内容 / Test | 步骤 / Steps | 预期结果 / Expected | 实际 / Actual | 状态 / Status |
|---|----------------|-------------|-------------------|-------------|--------------|
| 1 | 主菜单显示 / Main menu display | 启动程序 / Launch program | 显示 "aeacrA" 标题、按键提示、Press ENTER to start | 符合预期 / As expected | ✓ |
| 2 | 进入歌曲选择 / Enter song select | 主菜单按 ENTER / Press ENTER on menu | 显示歌曲列表 / Song list appears | 符合预期 / As expected | ✓ |
| 3 | 歌曲切换 / Switch song | 按 UP/DOWN 或 W/S / Press UP/DOWN or W/S | 选择高亮移动，显示歌名和BPM / Highlight moves, shows title and BPM | 符合预期 / As expected | ✓ |
| 4 | 手动游玩 / Manual play | 选中歌曲后按 ENTER / Press ENTER on selected song | 3秒倒计时后音符滚来 / 3s countdown, notes scroll toward hit line | 符合预期 / As expected | ✓ |
| 5 | 音符判定 / Note judgment | 在不同时机按键 / Press key at different timings | 显示 PERFECT/GREAT/GOOD/MISS | 符合预期 / As expected | ✓ |
| 6 | HOLD音符 / Hold notes | 按住对应键直到尾部 / Hold key until tail arrives | 头部尾部分别判定 / Head and tail judged separately | 符合预期 / As expected | ✓ |
| 7 | 分数与连击 / Score & combo | 连续击中音符 / Hit notes consecutively | 分数累计，连击增长并放大显示 / Score accumulates, combo scales up | 符合预期 / As expected | ✓ |
| 8 | MISS断连 / MISS breaks combo | 漏掉一个音符 / Miss a note | 连击归零 / Combo resets to 0 | 符合预期 / As expected | ✓ |
| 9 | 结算画面 / Results screen | 所有音符判定完毕 / All notes resolved | 显示判定数、总分、最大连击、等级 / Shows counts, score, max combo, grade | 符合预期 / As expected | ✓ |
| 10 | 返回主菜单 / Return to menu | 结算画面按 ENTER / Press ENTER on results | 回到主菜单 / Returns to main menu | 符合预期 / As expected | ✓ |
| 11 | 自动演示 / Auto demo | 歌曲选择中按 A / Press A in song select | 自动完美演奏 / Automatic perfect play | 符合预期 / As expected | ✓ |
| 12 | 退出游玩 / Quit playing | 游玩中按 ESC / Press ESC during play | 停止音乐，返回主菜单 / Stops music, returns to menu | 符合预期 / As expected | ✓ |
| 13 | 导入音频 / Import audio | 按I选择MP3文件 / Press I, select an MP3 | 文件选择器弹出，分析完成，歌曲出现 / Dialog opens, analysis completes, song appears | 符合预期 / As expected | ✓ |
| 14 | 游玩导入歌曲 / Play imported song | 选中导入歌曲按 ENTER / Press ENTER on imported song | 正常游玩，音乐播放 / Plays normally with background music | 符合预期 / As expected | ✓ |
| 15 | 随机生成谱面 / Random generated chart | 选中 Random 按 ENTER / Select Random, press ENTER | 游玩生成谱面，有节拍器 / Plays generated chart with metronome | 符合预期 / As expected | ✓ |
| 16 | 粒子特效 / Particle effects | 击中音符 / Hit a note | 爆炸粒子；combo>10出现火焰 / Explosion particles; fire at combo>10 | 符合预期 / As expected | ✓ |
| 17 | 屏幕闪光 / Screen flash | 获得PERFECT / Get PERFECT judgment | 屏幕短暂白色闪光 / Brief white screen flash | 符合预期 / As expected | ✓ |
| 18 | 节拍脉动 / Beat pulse | 正常游玩 / During normal play | 轨道随节拍闪烁 / Track pulses with the beat | 符合预期 / As expected | ✓ |
| 19 | 透视效果 / Perspective effect | 观察音符滚动 / Observe scrolling notes | 音符远小近大，3D隧道效果 / Notes grow as they approach | 符合预期 / As expected | ✓ |
| 20 | ESC返回 / ESC back | 歌曲选择中按 ESC / Press ESC in song select | 返回主菜单 / Returns to main menu | 符合预期 / As expected | ✓ |

---

## 已知问题 / Known Issues

- 导入极短的音频（<5秒）可能导致自动生成的谱面音符很少甚至分析失败
  Importing very short audio (<5s) may result in few notes or analysis failure

---

Guo Jiale (郭嘉乐) 2026/6/8
