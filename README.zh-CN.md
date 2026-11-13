<!-- “droidnative” 这个锚点让改名之前留下的链接继续有效：本项目在 2026-11-09 之前叫 droidnative。 -->
# <a id="droidnative"></a>DroidPlay Core

[English](README.md) · **简体中文**

[![Latest release](https://img.shields.io/github/v/release/enjoyerofslop/droidplay-core?label=latest%20release)](https://github.com/enjoyerofslop/droidplay-core/releases/latest)
[![License: MIT](https://img.shields.io/github/license/enjoyerofslop/droidplay-core)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-DroidPlay-5865F2?logo=discord&logoColor=white)](https://discord.gg/3r92f8wmh7)

**在安卓手机或掌机上，原生地玩你自己的 Switch 游戏。** DroidPlay 会把你手里那份 Switch 游戏打包成一个安卓应用：游戏的代码直接跑在手机的处理器上，而不是跑在模拟器里；画面由手机的 GPU 通过 Vulkan 绘制。

它面向的是有安卓手机或掌机、并且自己有 Switch 可以导出游戏的玩家。每款游戏你在电脑上构建一次，DroidPlay 负责把它装到手机上。DroidPlay Core 是它背后的引擎：[seedds/nxnative](https://github.com/seedds/nxnative)，该引擎让 Switch 游戏在 iPhone、iPad 和 Mac 上原生运行，其中的安卓移植版最早来自 [RogelioLB/nxnative-android](https://github.com/RogelioLB/nxnative-android)。

> [!IMPORTANT]
> **游戏请自备。** 本仓库不含任何游戏内容，也不分发打包好的游戏：游戏和密钥要从**你自己**的 Switch 里导出，构建出来的应用只供你自己使用。请不要分享内嵌了游戏的 APK（那里面带着游戏的代码和文件）、密钥或固件，也不要在 issue 里索要这些东西。本项目与任天堂以及任何游戏发行商都没有关联。

**下载 [DroidPlay for Windows](https://github.com/enjoyerofslop/droidplay-core/releases/latest)**：取最新 release 里的 **DroidPlay-Setup-&lt;version&gt;.exe**。运行它，剩下的步骤它带你走（[开始使用](#get-started)）。在 Mac 上请用 [DroidPlay](https://github.com/enjoyerofslop/droidplay)。

- **运行环境**：搭载 Android 10 或更高版本、GPU 支持 Vulkan 的 arm64 手机和掌机。已测试过高通 Adreno（Ayn Odin 2、Retroid Pocket 5、Galaxy S25 Edge 等）、Arm Mali（Pixel 9 Pro XL）和三星 Xclipse（Galaxy Z Flip 7）：[手机与掌机](#phones-and-handhelds)。
- **能玩什么**：[游戏状态](#game-status) 列出了在安卓上跑过的每一款游戏、跑在哪些设备上，以及跑到了哪一步。
- **求助**：[DroidPlay Discord](https://discord.gg/3r92f8wmh7)，遇到问题去 #help，想知道某款游戏在自己设备上跑得怎么样去 #compatibility。

<table>
<tr>
<td align="center" valign="top" width="50%"><img src="docs/images/windows/get-started.png" alt="DroidPlay for Windows 的“开始使用”页：已挑好密钥，构建工具正在下载并显示剩余时间，手机正在等待“允许”"><br><small><b>开始使用</b>：你的密钥、正在下载的工具、你的手机和你的第一款游戏</small></td>
<td align="center" valign="top" width="50%"><img src="docs/images/windows/library.png" alt="DroidPlay for Windows 的“库”：带着封面的《宝可梦 晶灿钻石》，已在 Galaxy S25 Edge 上就绪，带一个“开始游戏”按钮"><br><small><b>库</b>：装在手机上、可以随时开玩的游戏</small></td>
</tr>
</table>

[手机与掌机](#phones-and-handhelds) · [开始使用](#get-started) · [更新](#updating) · [在手机上](#on-your-phone) ·
[游戏状态](#game-status) · [帮助与反馈](#help-and-reports) · [指南](#guides) · [工作原理](#how-it-works) · [参与贡献](#contributing)

## <a id="phones-and-handhelds"></a>手机与掌机

DroidPlay 运行在 arm64 的安卓手机、掌机和平板上，要求 Android 10 或更高版本、GPU 支持 Vulkan。一款游戏跑得好不好取决于 GPU 和游戏本身：[游戏状态](#game-status) 给出了每款游戏在每台设备上的帧率。下面这些设备上跑过游戏：

| 设备 | 芯片 | GPU |
|---|---|---|
| Samsung Galaxy Z Fold 8 | Snapdragon 8 Elite Gen 5 | Adreno 840 |
| Samsung Galaxy S25 Edge | Snapdragon 8 Elite for Galaxy | Adreno 830 |
| OnePlus Pad 3 | Snapdragon 8 Elite | Adreno 830 |
| Ayn Odin 2 | Snapdragon 8 Gen 2 | Adreno 740 |
| Moto Razr Plus 2023 | Snapdragon 8+ Gen 1 | Adreno 730 |
| Retroid Pocket 5 | Snapdragon 865 | Adreno 650 |
| POCO X5 5G | Snapdragon 695 | Adreno 619 |
| Google Pixel 9 Pro XL | Google Tensor G4 | Arm Mali-G715 |
| Samsung Galaxy Z Flip 7 | Samsung Exynos 2500 | Samsung Xclipse 950 |

测试最多的是高通的 Adreno GPU；Mali 和 Xclipse 对本项目来说更新一些。POCO X5 5G 是最初那版移植所用的设备，最后一次运行在 2026-11-08 之前。其他设备可能也能跑，只是本项目还没测过：欢迎在 Discord 的 #compatibility 里说说某款游戏在你设备上的表现。

### <a id="another-vulkan-driver-turnip"></a>换用别的 Vulkan 驱动（Turnip）

在 Adreno GPU 上，游戏可以跑你自行装到手机上的 Vulkan 驱动，而不是系统自带的那个，就像 Switch 模拟器那样：通常是用 Mesa 开源的 Turnip 驱动编译出的版本（在三星 Xclipse GPU 上，则是 Mesa 为 Xclipse 编译的 RADV）。试一下不需要重新构建，有没有用取决于游戏和设备。步骤见：[另一个 Vulkan 驱动](docs/android.md#another-vulkan-driver-turnip)。

## <a id="get-started"></a>开始使用

### 你需要准备什么

- **一台用来构建的电脑**：DroidPlay for Windows 需要一台 64 位的 Windows 10（1809 或更高版本）或 Windows 11 电脑；Mac 上的 [DroidPlay](https://github.com/enjoyerofslop/droidplay) 需要一台 Apple 芯片、macOS 15 或更高版本的 Mac。在 Windows 上，DroidPlay 和它安装的工具约占 6 GB，而每款游戏的构建还要另占空间，占在存放该游戏文件的那个盘上：解压出的文件大约占游戏本身的体积，再加上着色器翻译期间所需的空间，大多数游戏最多约 20 GB，着色器超过 10 万条的（比如《宝可梦 Pokopia》）要 90 GB 甚至更多（[可用空间](docs/android.md#free-space)）。
- **一台安卓手机或掌机**，Android 10 或更高版本（[已测试的设备](#phones-and-handhelds)），一根 USB 线（或无线调试），以及装得下这款游戏的空间：它的文件会被复制到手机上（《弹丸论破 V3》是 6.7 GB）。
- **你自己的 Switch，以及从中导出的游戏和密钥**：游戏以 NSP 或 XCI 文件的形式放在一个文件夹里（本体游戏，以及你有的更新和 DLC，例如用 nxdumptool 导出），还有你 Switch 的 `prod.keys`（Lockpick_RCM）。Switch 2 游戏则从它的 `.nup` 文件或导出目录构建，不需要密钥；Switch 2 游戏在安卓上还处在早期阶段（[游戏状态](#game-status)）。

### 安装并构建你的第一款游戏

在 Windows 上：

1. **安装 DroidPlay。** 从[最新 release](https://github.com/enjoyerofslop/droidplay-core/releases/latest)下载 **DroidPlay-Setup-&lt;version&gt;.exe** 并运行。Windows 会警告说它来自网络、没有签名：选择**更多信息**，再选**仍要运行**。它只装到你当前的 Windows 用户下，不会弹管理员提示。
2. **跟着“开始使用”走。** DroidPlay 打开时是一张四步的清单。第一次配置大约要半小时。
   - **你的密钥**：选中你的 `prod.keys`。
   - **构建工具**：**安装工具**会下载 JDK、.NET SDK 和 Google 的 Android SDK（下载约 1.5 GB）。接受 Android SDK 的许可之前，DroidPlay 会先问你。
   - **你的手机**：打开 USB 调试，把手机插上，在手机上点**允许**。**设置我的手机**会给出你手机品牌对应的步骤。
   - **你的第一款游戏**：选中放着它 NSP 或 XCI 文件的文件夹（Switch 2 游戏则选放着它的 `.nup` 或导出目录的文件夹），然后点**构建并安装**。一款游戏第一次构建大约要 10 到 20 分钟；之后的构建会复用没有变动的部分。
3. **开玩。** 在 DroidPlay 的“库”里按**开始游戏**，或者在手机上打开 DroidPlay 应用挑一款游戏。游戏第一次启动要一分多钟，手机要在这期间准备好它的着色器；之后启动只要几秒。

应用的每一个页面、卸载、以及从源码运行：[DroidPlay for Windows](docs/android.md#droidplay-for-windows)。

### 在 Mac 上，或者用命令行

- **在 Mac 上**：[DroidPlay](https://github.com/enjoyerofslop/droidplay) 也能构建并安装安卓游戏：加上你的游戏文件夹，然后选**安装到安卓**（一个应用装下所有游戏，走 adb）或**构建游戏应用**。它的 README 里写了环境要求和配置步骤。
- **用命令行**，在 Windows、macOS 或 Linux 上：`scripts/build_android_from_nsp.py`（[用命令行打包](docs/android.md#packing-from-the-command-line)）。

## <a id="updating"></a>更新

- **DroidPlay for Windows** 有新版本时会提示：按**更新**，或者在**设置**的“更新”下面按**更新到 &lt;version&gt;**。它会下载新的 Setup、对照 release 校验、安装好再重新打开；你的游戏、构建和设置都保留。也可以关掉 DroidPlay，自己运行新的 Setup。
- **已经构建过的游戏**保持构建时的样子。想要某个 release 里的修复，就重新**构建并安装**一次；没变的部分不会重做，所以通常很快。存档留在手机上。
- 每个 release 的**变更内容**见 [release notes](https://github.com/enjoyerofslop/droidplay-core/releases)。

## <a id="on-your-phone"></a>在手机上

- **DroidPlay 应用**会列出手机上的游戏。挑一款进去改它的设置（主机模式、游戏语言、游戏支持的话还有渲染倍率、帧率计数器、震动），然后按**开始游戏**。
- **操作**：触屏控件以三种布局画在游戏画面之上——2D、3D 和 点按，用顶部的圆钮切换。接上手柄时，手柄作为 1P 使用，触屏控件会隐藏。
- **暂停与返回列表**：顶部的 **≡** 会暂停游戏并打开一个小菜单：继续游戏、触屏布局、帧率计数器、导出或导入存档、返回列表（在列表里对同一款游戏按**开始游戏**就会接着玩）。
- **存档**留在应用自己的存储里，所以更新应用不会丢。DroidPlay for Windows 可以在它的**手机**页面把存档备份到电脑上。
- **游戏应用**：DroidPlay for Windows 里的**管理 › 构建游戏应用…**会把一款游戏单独做成一个应用，有自己的图标和存档，可以拷到别的设备上安装。它只给你自己的设备用：里面带着游戏，绝不要分享出去。

更多：[安卓应用](docs/android.md#the-android-app) · [游戏应用](docs/android.md#game-apps)。

<!-- “status”这个锚点让改名之前留下的链接继续有效：DroidPlay 的 README 会链到 #status。 -->
## <a id="status"></a><a id="game-status"></a>游戏状态

哪些游戏能在安卓上跑、跑在哪些设备上，以及各自玩到了哪里。每一行都来自真机上的运行，由项目或贡献者完成。标为「可玩」的游戏，其所在行写明的那一段是被手工玩过的，存档和声音也检查过；下面几档精确说明了每个标签要求什么。

目前可玩：

- **可玩 – 有轻微问题**：Pokémon Brilliant Diamond、Pokémon Shield、Pokémon: Let's Go, Pikachu!、Persona 3 Portable、Divinity: Original Sin 2 - Definitive Edition、Mario Kart 8 Deluxe、Paper Mario: The Thousand-Year Door、Advance Wars 1+2: Re-Boot Camp。
- **可玩 – 有较严重问题**：Animal Crossing: New Horizons、Final Fantasy Resonance、Frostpunk、OCTOPATH TRAVELER、OCTOPATH TRAVELER II、Pokémon Legends: Arceus、The Legend of Zelda: Breath of the Wild、The Legend of Zelda: Link's Awakening、The Legend of Zelda: Skyward Sword HD、Xenoblade Chronicles 2、Xenoblade Chronicles 3。

还有更多游戏能进到游戏内（In-game）或者能进到它们的菜单；下表列出了在安卓上跑过的每一款游戏，以及看到的问题。

下面是测试运行时在设备上截的屏，按档位从高到低排列。顶部的圆钮是 DroidPlay 的菜单，底部那条线是安卓的手势条。在手机上，DroidPlay 的屏幕上控件是画在游戏画面之上的。每款游戏名下面的小图是其在下表中那一行的档位（各档位在截图下方有定义）。

<table>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/pokemon-brilliant-diamond-odin-2.jpg" width="256" alt="Ayn Odin 2 上《Pokémon Brilliant Diamond》的苑之镇"><br><small><b><a href="dm/games/0100000011D90000/README.md">Pokémon Brilliant Diamond</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Ayn Odin 2：苑之镇，60 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/pokemon-shield-galaxy-s25-edge.jpg" width="256" alt="Samsung Galaxy S25 Edge 上的《Pokémon Shield》：玩家站在化朗镇自家门口，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/01008DB008C2C000/README.md">Pokémon Shield</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Samsung Galaxy S25 Edge：化朗镇自家门外，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/pokemon-lets-go-pikachu-pixel-9-pro-xl.jpg" width="256" alt="Google Pixel 9 Pro XL 上的《Pokémon: Let's Go, Pikachu!》：玩家站在真新镇自家门外，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/010003F003A34000/README.md">Pokémon: Let's Go, Pikachu!</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Google Pixel 9 Pro XL：真新镇，30 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/divinity-original-sin-2-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《Divinity: Original Sin 2》：玩家角色在欢乐堡号船舱里"><br><small><b><a href="dm/games/010027400CDC6000/README.md">Divinity: Original Sin 2 - Definitive Edition</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Ayn Odin 2：欢乐堡号船舱，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/persona-3-portable-galaxy-z-flip-7.jpg" width="256" alt="Samsung Galaxy Z Flip 7 上的《Persona 3 Portable》，用的是一份下载来的存档：1 月 31 日，队伍在塔尔塔罗斯的入口大厅，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100DCD01525A000/README.md">Persona 3 Portable</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Samsung Galaxy Z Flip 7：塔尔塔罗斯入口（下载来的存档），60 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/mario-kart-8-deluxe-pixel-9-pro-xl.jpg" width="256" alt="Google Pixel 9 Pro XL 上的《Mario Kart 8 Deluxe》：马里奥在马力欧卡丁车体育场的第二圈跑在第一，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100152000022000/README.md">Mario Kart 8 Deluxe</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Google Pixel 9 Pro XL：马力欧卡丁车体育场，60 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/paper-mario-the-thousand-year-door-galaxy-s25-edge.jpg" width="256" alt="Samsung Galaxy S25 Edge 上的《Paper Mario: The Thousand-Year Door》：马里奥在剧场舞台上的第一场战斗，对手是克朗普领主，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100ECD018EBE000/README.md">Paper Mario: The Thousand-Year Door</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Samsung Galaxy S25 Edge：第一场战斗，对克朗普领主，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/advance-wars-1-2-re-boot-camp-moto-razr-plus-2023.jpg" width="256" alt="Moto Razr Plus 2023 上的《Advance Wars 1+2: Re-Boot Camp》：野战训练第一课的战斗场面，橙星步兵对阵蓝月步兵，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100300012F2A000/README.md">Advance Wars 1+2: Re-Boot Camp</a></b><br><a href="#tiers"><img src="docs/badges/playable-minor.svg" height="20" alt="可玩 – 有轻微问题"></a><br>Moto Razr Plus 2023：野战训练的第一场战斗，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/animal-crossing-new-horizons-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《Animal Crossing: New Horizons》：第一个晚上的欢迎会，玩家在篝火旁和豆狸、粒狸、狸克以及两位岛民在一起"><br><small><b><a href="dm/games/01006F8002326000/README.md">Animal Crossing: New Horizons</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Ayn Odin 2：第一个晚上的欢迎会，30 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/zelda-skyward-sword-hd-odin-2.jpg" width="256" alt="Ayn Odin 2 上《The Legend of Zelda: Skyward Sword HD》的天空阁广场，林克站在鸟像前"><br><small><b><a href="dm/games/01002DA013484000/README.md">The Legend of Zelda: Skyward Sword HD</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Ayn Odin 2：天空阁，60 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/final-fantasy-resonance-odin-2.jpg" width="256" alt="Ayn Odin 2 上《Final Fantasy Resonance》夜晚的第一片原野，火焰沿着道路绘出"><br><small><b><a href="dm/games/0100606026F12000/README.md">Final Fantasy Resonance</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Ayn Odin 2：第一片原野，火焰已绘出，52 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/frostpunk-galaxy-s25-edge.jpg" width="256" alt="Samsung Galaxy S25 Edge 上《Frostpunk》的城市：陨石坑里的能量塔和它旁边的残骸，覆着雪"><br><small><b><a href="dm/games/0100B1C0249B4000/README.md">Frostpunk</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Samsung Galaxy S25 Edge：城市，30 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/zelda-breath-of-the-wild-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《The Legend of Zelda: Breath of the Wild》：林克在复苏神庙里"><br><small><b><a href="dm/games/01007EF00011E000/README.md">The Legend of Zelda: Breath of the Wild</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Ayn Odin 2：复苏神庙，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/octopath-traveler-pixel-9-pro-xl.jpg" width="256" alt="Google Pixel 9 Pro XL 上的《OCTOPATH TRAVELER》：海茵特在斯瓦奇村的「挑衅」战斗中对抗新手猎人，她的指令菜单开着"><br><small><b><a href="dm/games/010057D006492000/README.md">OCTOPATH TRAVELER</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Google Pixel 9 Pro XL：斯瓦奇村的一场「挑衅」战斗，57–60 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/octopath-traveler-ii-galaxy-z-flip-7.jpg" width="256" alt="Samsung Galaxy Z Flip 7 上的《OCTOPATH TRAVELER II》：光在战场上的第一场战斗，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100A3501946E000/README.md">OCTOPATH TRAVELER II</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Samsung Galaxy Z Flip 7：光的第一场战斗，56–60 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/pokemon-legends-arceus-oneplus-pad-3.jpg" width="256" alt="OnePlus Pad 3 上的《Pokémon Legends: Arceus》，新开一局：玩家在起始海滩边的巨石旁把精灵球扔向火球鼠，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/01001F5010DFA000/README.md">Pokémon Legends: Arceus</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>OnePlus Pad 3：第一次捕捉，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/xenoblade-chronicles-2-galaxy-z-flip-7.jpg" width="256" alt="Samsung Galaxy Z Flip 7 上的《Xenoblade Chronicles 2》：教学战斗开始时船甲板上的帝王蟹怪，莱克斯在前，绘制干净，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0100E95004038000/README.md">Xenoblade Chronicles 2</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Samsung Galaxy Z Flip 7：帝王蟹怪的战斗，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/zelda-links-awakening-retroid-pocket-5.jpg" width="256" alt="Retroid Pocket 5 上的《The Legend of Zelda: Link's Awakening》，新开一局：林克在托隆波海岸的水边举起剑"><br><small><b><a href="dm/games/01006BB00C6F0000/README.md">The Legend of Zelda: Link's Awakening</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Retroid Pocket 5：取得剑，30 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/xenoblade-chronicles-3-galaxy-s25-edge.jpg" width="256" alt="Samsung Galaxy S25 Edge 上的《Xenoblade Chronicles 3》：诺亚一行在永烬平原的第一场战斗中对抗阿格努斯士兵，地面和岩石绘制干净，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/010074F013262000/README.md">Xenoblade Chronicles 3</a></b><br><a href="#tiers"><img src="docs/badges/playable-major.svg" height="20" alt="可玩 – 有较严重问题"></a><br>Samsung Galaxy S25 Edge：第一场战斗，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/super-mario-odyssey-retroid-pocket-5.jpg" width="256" alt="Retroid Pocket 5 上《Super Mario Odyssey》的开场动画"><br><small><b><a href="dm/games/0100000000010000/README.md">Super Mario Odyssey</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Retroid Pocket 5：开场动画，59 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/super-smash-bros-ultimate-odin-2.jpg" width="256" alt="Ayn Odin 2 上《Super Smash Bros. Ultimate》的一场战斗"><br><small><b><a href="dm/games/01006A800016E000/README.md">Super Smash Bros. Ultimate</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Ayn Odin 2：一场战斗，40–59 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/dark-souls-remastered-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《DARK SOULS: REMASTERED》：玩家在不死院牢房里"><br><small><b><a href="dm/games/01004AB00A260000/README.md">DARK SOULS: REMASTERED</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Ayn Odin 2：不死院牢房，30 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/blasphemous-2-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《Blasphemous 2》：忏悔者在三座雕像的房间里"><br><small><b><a href="dm/games/010040801A4C8000/README.md">Blasphemous 2</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Ayn Odin 2：三座雕像的房间，60 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/donkey-kong-country-returns-hd-odin-2.jpg" width="256" alt="Ayn Odin 2 上的《Donkey Kong Country Returns HD》：大金刚在 1-1 Jungle Hijinxs 的沙滩上"><br><small><b><a href="dm/games/01009D901BC56000/README.md">Donkey Kong Country Returns HD</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Ayn Odin 2：1-1 Jungle Hijinxs，60 fps</small></td>
</tr>
<tr>
<td align="center" valign="top" width="33%"><img src="docs/images/android/mario-kart-world-oneplus-pad-3.jpg" width="256" alt="OnePlus Pad 3 上的《Mario Kart World》：马里奥在马力欧兄弟赛道的第三圈跑在第七，赛道表面没有贴图，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0400C3F00006E000/README.md">Mario Kart World</a></b><br><a href="#tiers"><img src="docs/badges/in-game-blocked.svg" height="20" alt="游戏内，受阻"></a><br>OnePlus Pad 3：马力欧兄弟赛道的一场比赛，15–21 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/zelda-ocarina-of-time-galaxy-z-fold-8.jpg" width="256" alt="Samsung Galaxy Z Fold 8 上的《The Legend of Zelda: Ocarina of Time》：少年林克和娜薇走在穿越科奇里森林的路上，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/0400486024DEC000/README.md">The Legend of Zelda: Ocarina of Time</a></b><br><a href="#tiers"><img src="docs/badges/in-game-blocked.svg" height="20" alt="游戏内，受阻"></a><br>Samsung Galaxy Z Fold 8：科奇里森林，15–17 fps</small></td>
<td align="center" valign="top" width="33%"><img src="docs/images/android/assassins-creed-black-flag-moto-razr-plus-2023.jpg" width="256" alt="Moto Razr Plus 2023 上《Assassin's Creed IV: Black Flag》开场的暴风雨：爱德华在雨中的船甲板上，屏幕上叠着触屏控件"><br><small><b><a href="dm/games/010044700DEB0000/README.md">Assassin's Creed: The Rebel Collection</a></b><br><a href="#tiers"><img src="docs/badges/in-game.svg" height="20" alt="游戏内"></a><br>Moto Razr Plus 2023：黑旗的海上开场，30 fps</small></td>
</tr>
</table>

<a id="tiers"></a>
每一行的「状态」以它的档位开头：即条件全部被证实过的、最高的那一档。两个「可玩」档都写明了游戏玩到哪一步（“走到……”），但都不表示整款游戏都玩过了。

| 档位 | 已证实的内容 |
|---|---|
| **可玩 – 有轻微问题**，走到*指定的那一段* | 满足「可玩 – 有较严重问题」的全部要求，并且在至少一台设备上走过那一段：帧率中位数不低于目标帧率的 95%，且没有哪个 30 秒区间的中位数低于它的 90%（加载、切换场景、以及第一次启动时的着色器与管线构建除外）；只有观感上的瑕疵（单帧的伪影、略偏的颜色或明暗、只在首次启动构建管线时才缺的绘制），且每处都与 Mac 对比过；没有崩溃或卡死；声音正常；「继续游戏」能载入最新的存档；而这一段要覆盖到游戏的第一次战斗、比赛或关卡结束 |
| **可玩 – 有较严重问题**，走到*指定的那一段* | 从新游戏或安卓上存的存档起，手工玩过（adb 注入的输入不算；只靠脚本跑一遍不算）指定的那一段（在另一台安卓设备上手工存的存档算数，在 Mac 上存的不算）；帧率不低于目标帧率的一半（中位数）；这一段走完，最多一次崩溃或卡死，靠重启加「继续游戏」过去、且没有再回到同一点；安卓上存的存档在冷启动后能重新载入；声音检查过。这一行会列出每一处让它止步于「有轻微问题」的问题 |
| **游戏内** | 玩家可以操控的实际游玩，而不只是菜单或影片，画面可用，帧率不低于目标的一半，但还没被证实为可玩：脚本运行、别人的存档或 Mac 上存的存档、没有手工玩过一段、或者存档／声音没检查 |
| **游戏内，受阻** | 进得去游玩，但有已知的 bug 阻断正常玩：世界缺失或全黑、帧率不到目标的一半、或者在同一处反复崩溃／卡死 |
| **菜单** | 标题画面、菜单或影片；游玩中没有玩家操控 |
| **能启动** | 出过第一帧或一个 Logo；再往后没有证实 |
| **跑不起来** | 在第一帧之前就停住，或者打包脚本不接受它 |

目标帧率是这款游戏在安卓上默认的帧率：取它 profile 的 `android_defaults.txt` 里的 `DM_FPS_TARGET`，没有就取 profile 的 `fps_target`，再没有就取 Switch 上的帧率。一行的档位以表现最多的那台设备为准，行内也会写明其他设备的表现。

每一行的其余部分说明：跑在哪几台设备上、玩到多远、怎么玩的（手工，还是从全新存档或下载来的存档跑的脚本）、帧率、看到的问题，以及还没试过的部分。

| 游戏 | 设备 | 状态 |
|---|---|---|
| Pokémon Brilliant Diamond 1.3.0 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7、Google Pixel 9 Pro XL、Moto Razr Plus 2023 | 可玩 – 有轻微问题，走过睿智湖的第一场战斗：60 fps（这是 profile 的帧率，Switch 上是 30）。在 Pixel 9 Pro XL（Mali）、Moto Razr Plus 2023（Adreno 730）和 Samsung Galaxy Z Flip 7（Xclipse）上，从新游戏手工玩过：穿过双叶镇、201 号道路和睿智湖，到图特龟和第一场对野生的姆克儿的战斗并取胜，声音正常，手机上存的存档和「继续游戏」都能用；在 Z Flip 7 上，32 分钟内 59.8 fps（没有哪个 30 秒区间低于 57.9），双叶镇的池塘自 #204 起被画成了水。问题：在 Pixel 上，初始精灵选择画面有一分钟是 50–54 fps；Razr 和 Z Flip 7 上没看到问题。其余四台是「游戏内」：苑之镇大地图 59–60 fps，是在下载来的存档里跑的脚本，玩家站在宝可梦中心旁；Odin 2 上曾在 2026-11-07 手工玩新游戏进到大地图，那是在并入 nxnative 之前，之后没有再玩。Retroid Pocket 5 已不再一启动就崩溃，它自己的驱动现在跑苑之镇和 [Turnip](#another-vulkan-driver-turnip) 一样快（此前 15 fps） |
| Animal Crossing: New Horizons 3.0.3 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge | 可玩 – 有较严重问题，走过第一天的白天与夜晚、到第二天早上：在 Ayn Odin 2 上，从新游戏手工玩过捏人、乘机抵达、狸克的欢迎与帐篷、捡树枝和苹果做篝火、欢迎会（岛上正是在那里命名的）、帐篷里的第一夜和第二天早上的 NookPhone，30 fps（与 Switch 相同；2 小时 12 分的这次运行平均 30.00，没有哪个区间低于 29.8），声音正常，当天早上存的游戏第一份存档在冷启动后由「继续游戏」载入（[它的说明](dm/games/01006F8002326000/README.md#android-through-the-first-night-on-the-odin-2)）。问题：岛上最初的几帧绘制时，驱动的卡死恢复截短了一次 GPU 提交（一帧 368 ms；早前一次运行里有三帧），没有与 Mac 对比。还没到「有轻微问题」：那处故障没有与 Mac 对比，而且这一段里没有战斗、比赛或关卡结束——这款游戏本来也没有这些。脚本运行：四台上都是 30 fps，位置是新游戏时的机场（全新存档、无输入），以及下载来的存档里玩家站立的自家门外 |
| Super Mario Odyssey 1.4.1 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge、Google Pixel 9 Pro XL | 游戏内：五台上「开始」菜单和开场动画都是 59–60 fps（Retroid Pocket 5 在 2026-11-08 跑这段动画时是 38），在 Odin 2 上还能在库巴王国游玩，60 fps（一次 15 秒的脚本运行），越过了过去会让它崩溃的提示影片（那是宿主机的 AVC 解码器，已修好；Pad 3 上影片也能播）。没有手工玩过。加载时偶发的崩溃已修好。Pixel 9 Pro XL 的 Mali-G715 是第一个非 Adreno 的 GPU，它没有 BC 纹理，所以纹理在 CPU 上解码（动画期间常驻 2.2 GB，对比 1.64 GB） |
| Super Smash Bros. Ultimate 13.0.5 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge | 游戏内：四台都能启动到开场影片，60 fps，用的是打包器现在会带上的共享字体（安卓自带的 Roboto 会让它崩溃）；大约每五次启动就有一次的崩溃也已修好。路线里那场对战（马里奥对随机 CPU 角色，玩家不动；没有手工玩过）按场景和角色不同：S25 Edge 上 60 fps，Pad 3 上 52–60（2026-11-09），Retroid Pocket 5 上 57–60（2026-11-10），Odin 2 上 40–59（2026-11-08，之后没再测） |
| The Legend of Zelda: Link's Awakening 1.1.0 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge | 可玩 – 有较严重问题，走过托隆波海岸、取得剑以及最初的几场战斗：在 Retroid Pocket 5 上（2026-11-12），通过 adb 从新游戏玩过玛林的家、塔林的盾、梅贝村和被围墙的田地，到托隆波海岸和剑，然后用剑砍掉了两只海胆怪和两只沙蟹。从 Game Over 画面存进存档位 1，冷启动后按 Start，林克带着剑回到海滩。声音正常（22 分钟里有 5 次短暂欠载），每次启动有一行红色日志但画面上看不出问题，没有崩溃。玛林家门外那段梅贝村与 Mac 的画面一致，连日照阴影都对得上（[它的说明](dm/games/01006BB00C6F0000/README.md#android)）。让它止步于「有轻微问题」的原因：到了房子外面，Retroid Pocket 5 会掉到游戏的 30 fps 间隔（中位数 31–32 fps 对 60；玛林的屋里是 59）。OnePlus Pad 3 在修好日照之前，手工玩了同一段到取得剑：屋里和村里 60 fps，田地和海滩上掉到 30 fps 间隔。还没试：神秘森林。从下载来的存档在远古遗迹（第五个迷宫之后）站着不动：Odin 2 上 60 fps，S25 Edge 上 38–45，Pad 3 和 Retroid Pocket 5 上 32–33，后两者上游戏会掉到它的 30 fps 间隔。它在 Retroid Pocket 5 上每次启动都崩、在 Pad 3 上偶发的启动崩溃已修好（已在 Retroid Pocket 5 上确认） |
| The Legend of Zelda: Skyward Sword HD 1.0.1 | Ayn Odin 2、OnePlus Pad 3、Retroid Pocket 5、Samsung Galaxy S25 Edge | 可玩 – 有较严重问题，走过开场进入天空阁（ instructor Horwell 的入门课）：在 Retroid Pocket 5 上，用手柄操作从新游戏手工玩过开场、林克的房间、骑士学院，一直到天空阁，60 fps（标题卡上是 30），声音正常，冷启动后自动存档由「继续游戏」载入。开始这局新游戏那次会话里，天空阁有几处画成平的或干脆没画出来（Horwell 的木箱在原野开场镜头里是平的一块洋红），这些问题在 0.7.6 之后的 main 上已修好，但还没进 release（[#270](https://github.com/enjoyerofslop/droidplay-core/pull/270)；新游戏玩到天空阁的开场镜头时绘制正常）。还没到「有轻微问题」：这一段没有覆盖游戏的第一次战斗、比赛或关卡结束（[它的说明](dm/games/01002DA013484000/README.md#android-a-new-game-on-the-retroid-pocket-5)）。从一份下载来的 31 小时英雄模式存档，天空阁广场上林克站在鸟像前，四台的地形都是彩色的：Odin 2、Pad 3 和 S25 Edge 上 59–60 fps，Retroid Pocket 5 上 43（2026-11-10），在那里同一次运行中游戏还会在 60 和 30 fps 两个间隔之间来回切。开场影片 55–60 fps（Retroid Pocket 5 上 41） |
| Final Fantasy Resonance 1.0.1 | Ayn Odin 2、OnePlus Pad 3、Samsung Galaxy S25 Edge、Google Pixel 9 Pro XL | 可玩 – 有较严重问题，走过新游戏的开场、第一片原野和它的头三场战斗：在 Ayn Odin 2 上，从新游戏手工玩过；自 `ANDROID_CHAIN` 6 起原野的火焰能画出来，chain 6 上帧率中位数 52 fps（30 秒区间内 43–60），声音正常，冷启动后自动存档由「继续游戏」载入（[它的说明](dm/games/0100606026F12000/README.md#android-a-new-game-by-hand-on-the-odin-2)）。问题：帧率不到 60 目标的 95%；离镜头最近的火焰被画成粗糙的色块，岩石贴图上有千鸟格状的条纹和淡淡的横线，这些都还没与 Mac 对比。脚本运行：Odin 2 和 Pad 3 上原野里约 42 fps，S25 Edge 上 30–33（0.6.0 之前是 10–16 fps），Pixel 9 Pro XL 上开场 30 fps。没在 Retroid Pocket 5 上试过 |
| Pokémon Shield 1.3.2 | Retroid Pocket 5、Samsung Galaxy S25 Edge、Google Pixel 9 Pro XL、Samsung Galaxy Z Flip 7 | 可玩 – 有轻微问题，走过 2 号道路进到木兰博士的家：四台都是 30 fps（与 Switch 相同）。在 Z Flip 7（Xclipse）上，从新游戏手工玩过开场、1 号道路、木杆镇和御三家，到与霍普的对战并取胜，然后进到微寐森林，在那里打了一场野外战斗；在 Retroid Pocket 5 上玩到与霍普的对战并取胜，再从 Z Flip 7 的森林存档走过森林里的事件（雾中的战斗、丹帝的救援）回到木杆镇见妈妈，再从那里穿过木杆镇（图鉴）、2 号道路和它的头几个训练家，进到木兰博士的家；在 S25 Edge 和 Pixel 9 Pro XL（Mali）上，进到木杆镇，霍普在自家门外遇到玩家。声音、手机上存的存档和「继续游戏」在四台上都正常。问题：首次启动时的管线构建（Z Flip 7 上有一帧 6.4 s、Retroid Pocket 5 上有一帧 5.0 s；下次启动最多 118 和 178 ms），以及首次进入实验室和 2 号道路构建管线时出现的 1.4–1.7 s 的帧；其他问题没看到。没玩到木兰博士花园里的那场对战和旷野地带；也没在其他设备上试过 |
| Frostpunk 1.0.1 | Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7、Moto Razr Plus 2023 | 可玩 – 有较严重问题，走过第一天进到第一夜：S25 Edge（Adreno）和 Galaxy Z Flip 7（Xclipse）上都是 30 fps（除加载外每个 30 秒区间 29.1–29.7）；在 S25 Edge 上，通过 adb 从「新家园」的新游戏手工玩过：采集煤、木材和钢材，建成三座帐篷、放置一座伙房，启动能量塔，度过第一个工作日进入夜晚，声音正常（做过音频转储：全程有声），手机上存的存档和「继续剧情」在冷启动后都能载入。能量塔、建筑和道具都通过 raw global memory 绘制，这是它 profile 里打开的一项。问题：这一段远在剧本结束之前就完了；S25 上开场视野的截图看着比 Mac 的截图更暗，没有在同一捕获条件下对比。在 Galaxy Z Flip 7（Xclipse）上，从新游戏手工玩过同一段到第一夜，存档并在冷启动后继续，城市的 30 秒区间里 29.0–29.7 fps，声音正常（做过音频转储）。在 Moto Razr Plus 2023（Adreno 730，高通驱动 V@0615.98）上，从标题画面用脚本路线进到城市，29.5 fps，能量塔和残骸都画了出来：该驱动的编译器不接受着色器读取 raw global memory 用的指针（`OpConvertUToPtr not supported`），所以那里改成通过 storage buffer 数组访问内存。没有玩过教程的第一个弹窗之后，声音也没在那里复查 |
| Pokémon: Let's Go, Pikachu! 1.0.0 | Samsung Galaxy Z Fold 8、Google Pixel 9 Pro XL、Samsung Galaxy Z Flip 7 | 可玩 – 有轻微问题，走过常磐市和对手的第一场对战（大木的包裹）：三台都是 30 fps（与 Switch 相同）。在 Z Fold 8 上，从手机在真新镇存的存档手工玩过大木博士的剧情、拿到皮卡丘、他的研究所和图鉴，在 1 号道路上按键完成两次野外捕捉（不需要体感）；进到真新镇的那段开场在那里是脚本运行。在 Pixel 9 Pro XL（Mali）上，从新游戏手工玩过开场和对手来访进到真新镇，并从 Z Fold 8 的存档在 1 号道路抓到一只野生波波。然后从那份存档手工玩过 1 号道路（更多捕捉）到常磐市，把商店店员的大木包裹送回大木博士，再到研究所里与对手的第一场对战（他的伊布，用电击取胜），在 35 分钟的一次运行里每分钟都是 29.6–30.0 fps，之后存的存档在冷启动后由「继续游戏」载入。在 Z Flip 7（Xclipse）上，从新游戏手工玩过开场进到卧室，再从 Pixel 的存档在战后穿过 1 号道路（赢了训练家对战）、常磐市和 2 号道路进到常磐森林，在那里存的存档在冷启动后由「继续游戏」载入。声音（经音频转储确认）、手机上存的存档和「继续游戏」在三台上都正常。问题：一直到对手那场对战都没看到问题。在 Z Flip 7 上，走过常磐森林第一个捕虫少年那段每次 40–90 秒里只有 21–28 fps（这是游戏自己的逐帧处理；没有与 Mac 对比），所以森林这段不算进「有轻微问题」的那一段；之后在那里的一次运行中，森林画面下方三分之一出现了一条平坦的暗带，尚未与其他手机或 Mac 对比（[它的说明](dm/games/010003F003A34000/README.md#android)）。还没试：宝可梦中心和商店内部、常磐森林的训练家与尼比市、体感瞄准、其他设备 |
| Divinity: Original Sin 2 - Definitive Edition 1.0.3.1 | Ayn Odin 2、OnePlus Pad 3、Google Pixel 9 Pro XL | 可玩 – 有轻微问题，走过甲板下的第二场战斗（锁着的油腻门之前）：这款游戏自己的 30 fps，从新游戏穿过捏人和开场动画进到欢乐堡号的船舱，然后手工玩到客舱甲板，在 Odin 2 上穿过着火的船舱到顶层甲板的第一场战斗（两只虚空觉醒者，获胜）、救生艇和它的对话，以及甲板下的第二场战斗（虚空幼体，用洛思和野兽取胜），声音正常，快速存档的时间按宿主机的时钟标记，冷启动后「继续游戏」载入最新的那份。每个区间的帧时间中位数 33.1–33.5 ms；日志里有四行 alpha 测试的红字，屏幕上没有异常。在 Pixel 9 Pro XL（Mali）上，顶层甲板的第一场战斗也赢了，同样 30 fps，声音正常，冷启动后「继续游戏」可用；它的 GPU 在这 33 ms 的帧里占约 26 ms（[它的说明](dm/games/010027400CDC6000/README.md#on-the-pixel-9-pro-xl)）。在 Pad 3 上改一个设置就能跑 40 或 60 fps，两种帧率下游戏都按真实时间推进，并且稳定跑了 25 分钟的 60 fps（[它的说明](dm/games/010027400CDC6000/README.md#frame-rate)）。没玩到欢乐堡 |
| The Legend of Zelda: Breath of the Wild 1.9.0 | Ayn Odin 2、OnePlus Pad 3、Samsung Galaxy S25 Edge、Samsung Galaxy Z Fold 8 | 可玩 – 有较严重问题，走过复苏神庙、上到初始台地（尚无战斗）：Odin 2 上 30 fps（它的安卓目标），从新游戏手工玩过：在神庙里醒来，取走希卡石板，打开神庙的门走出来，然后是海拉鲁上空的动画和台地上最初的几分钟，声音正常，手机上存的自动存档在冷启动后由「继续游戏」载入。没有走到那位老人（[它的说明](dm/games/01007EF00011E000/README.md#android)）。问题：这一段在第一次战斗之前就结束了；林克摔死那一帧里附近岩石上有红色涂抹，没有与 Mac 对比。从 Mac 上存的存档进神庙：Pad 3 和 S25 Edge 在其安卓默认设置下是 30 fps（描述符集重新绑定、命令录制器、30 fps 目标）；Galaxy Z Fold 8 上是 24，它的 GPU 一帧要 30 ms。在 Pad 3 上曾在原野的第一帧就丢掉 GPU，两块 Adreno 830 上都把神庙画得发暗：两处都已修好，分别在 S25 Edge 上、以及在 Pad 3 上用 main 的 0.7.5 构建从新游戏手工验证：神庙是亮的，在台地上约 5.5 分钟没有丢 GPU，30 fps，存档在冷启动后由「继续游戏」载入。要做到 60 fps 需要重放的 CPU 时间和 GPU 时间都降下来 |
| OCTOPATH TRAVELER 1.0.3 | Google Pixel 9 Pro XL、Retroid Pocket 5 | 可玩 – 有较严重问题，走过海茵特最初的几场战斗：在 Pixel 9 Pro XL（Mali-G715，Android 17）上，通过 adb 从新游戏玩过海茵特的开场（回忆和斯瓦奇村）、村长、路径行动教学，以及对新手猎人的两场「挑衅」战斗并取胜，然后在村里的存档碑存了档，冷启动后由「继续游戏」载入，再走到通往低语森林的路上与第一只怪物（一只睡鼠）的第一场战斗（破防并击败），声音正常，没有崩溃（[它的说明](dm/games/010057D006492000/README.md#android)）。用从 1.0.5 派生的 profile 从卡带的 1.0.3 构建；着色器切分找到了全部 5,434 个着色器。目标是 60 fps（Switch 上是 30）：战斗和低语森林能保持 57–60，而从新游戏到存档的中位数是 52.1 fps，从「继续游戏」到睡鼠是 58.7。峰值 3.4 GB（进程的内存 cgroup），远低于 Android 17 的 8 GiB 上限；从未被杀。问题：在斯瓦奇村，Mali 的 GPU 一帧要 17–19 ms，所以村子只有 44–57 fps，它的存档界面是 38；通往低语森林的路上，画面上下两侧模糊前景与背景相接处有发白的锐边区域，没有与 Mac 对比（那里也没玩到那么远）。还没到「有轻微问题」：中位数不到 57 fps，而那些区域没对比过。在 Retroid Pocket 5（Adreno 650）上，在给 Adreno 6xx 的小型分层渲染通道分配临时颜色槽位之前，每次启动都在驱动里崩溃；修好之后，从新游戏走海茵特的回忆进到斯瓦奇村约 49 fps，调色与 Pixel 上一致（没有再往下玩）。没在其他设备上试过 |
| OCTOPATH TRAVELER II 1.0.0 | Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7 | 可玩 – 有较严重问题，走过光的第一场战斗：在 S25 Edge（Adreno 830）上，通过 adb 从新游戏玩过初始设置、光的开场和战场上的第一场战斗及教学（获胜），然后在战场上自由行动、又打了两场战斗，声音正常、没有崩溃，战场上游戏自己的自动存档在冷启动后由「继续游戏」载入；在 Galaxy Z Flip 7（Xclipse 950）上同样如此（[它的说明](dm/games/0100A3501946E000/README.md#android)）。用从 1.1.1 派生的 profile 从卡带的本体 1.0.0 构建；它的 13,942 个着色器全部翻译。目标是 60 fps（Switch 上是 30）：两台手机上的战斗、剧情和营地都能保持 56–60，S25 Edge 的 30 秒区间中位数是 59.1。PSS 3.2–3.3 GB，从未被杀。问题：战场上的俯视原野（一帧 1,700–2,050 次绘制）只有 43–50 fps，不到目标的 90%；没有与 Mac 对比。在两台手机上，战场的土地、岩石和营地的地面都曾被画成水平的条纹，直到模板模式下的纹理槽位开始读取模板缓冲（修好之后 S25 Edge 的地面干净，帧率也没有损失）。序章里的下一场战斗——雷梅与骑马将军的对战——被 agent 的普通攻击打输了；没有再往下玩。没在其他设备上试过 |
| Persona 3 Portable 1.0.2 | Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7 | 可玩 – 有轻微问题，走过第一场战斗（4 月 9 日的天台）：两台都是 60 fps（与 Switch 相同），从新游戏手工玩过开场、宿舍和最初几天学校生活（含点击式探索），到 4 月 9 日晚上和第一场战斗并按键取胜，声音正常，在宿舍签到表存的存档和「继续游戏」都能用。S25 Edge 上是主机模式，Z Flip 7（Xclipse）上是安卓默认的掌机模式，两者都可用（[它的说明](dm/games/0100DCD01525A000/README.md#android)）。问题：S25 Edge 上没看到问题；Z Flip 7 上开场影片有一帧盖满细密的点阵，没有与 Mac 对比。没玩过第一场战斗之后（塔尔塔罗斯）；也没在其他设备上试过 |
| Mario Kart 8 Deluxe 4.0.1 | Google Pixel 9 Pro XL、Samsung Galaxy Z Fold 8、Moto Razr Plus 2023、OnePlus Pad 3 | 可玩 – 有轻微问题，走过第一场 50cc 比赛（马力欧卡丁车体育场的蘑菇杯）：在 Pixel 9 Pro XL 上，在马力欧卡丁车体育场跑了两场 50cc 大奖赛并都获胜，60 fps（与 Switch 相同），从一份新存档开始：启动、标题画面的演示比赛、选 Mii（头部是空的，与 Mac 相同）、带影片预览的菜单，然后是比赛；存档在冷启动后能载入，声音正常。那几场比赛是靠游戏自带的智能转向、通过 adb 一直按住加速键跑完的；在 Samsung Galaxy Z Fold 8 上（项目所有者）则是手工转向跑完的，转向操作符合预期。Mali GPU 没有 BC 纹理，所以在 CPU 上解码：常驻 4.3 GB，而 Mac 上是 2.4。问题：在 Moto Razr Plus 2023（Adreno 730）上一场比赛约 45 fps，瓶颈在重放的 CPU；在那里，修好赛道加载时的崩溃之后（[#243](https://github.com/enjoyerofslop/droidplay-core/pull/243)），演示比赛、一场 50cc 比赛跑到成绩画面、以及冷启动后载入存档都跑通了，占用 1.6 GB，标题和菜单是 60。在 OnePlus Pad 3（Adreno 830）上，同样的修复之后：两场演示比赛和蘑菇杯的前两场比赛（马力欧卡丁车体育场和水上乐园）跑到成绩画面都是 60 fps，GPU 一帧约 8.5 ms，2.6 GB，没有红色日志，冷启动后存档也能载入（[它的说明](dm/games/0100152000022000/README.md#android)） |
| Paper Mario: The Thousand-Year Door 1.0.0 | Samsung Galaxy S25 Edge | 可玩 – 有轻微问题，走过第一场战斗（欢乐之城的克朗普领主，含栗宝宝的教程）：在 S25 Edge 上，通过 adb 从一个新存档手工玩过故事书序章、欢乐之城里的碧琪、马里奥的家和船进到欢乐之城码头，赢下第一场战斗，栗宝宝在广场加入，37 分钟里帧率中位数 29.9 fps（30 秒区间内 27.8–30.0；这是游戏自己的 30 fps），声音正常（序章影片走的是它自己的输出），没有崩溃，战斗后在广场的存档砖上存的档在冷启动后由「继续游戏」载入。它需要 [#337](https://github.com/enjoyerofslop/droidplay-core/pull/337)（已在 main 上，还没进 release）：没有它，低内存杀手会在序章的海上场景杀掉游戏，那时它的描述符池占到 6.7 GB。导出的是 1.0.0 卡带本体，用从 1.0.1 派生的 profile 打包，所以 1.0.1 的 60 fps 补丁用不上（[它的说明](dm/games/0100ECD018EBE000/README.md#android)）。没有看出不对的地方；序章的场景与同一构建在 Mac 上同一批帧的截取一致。没在其他手机上试过 |
| Advance Wars 1+2: Re-Boot Camp 1.0.0 | Moto Razr Plus 2023、Samsung Galaxy Z Flip 7 | 可玩 – 有轻微问题，走过野战训练的第一课（部队指令）：在 Moto Razr Plus 2023（Adreno 730，高通自家驱动）上，通过 adb 从新游戏玩过 Bink 开场影片、内尔的介绍和一场新的休闲战役到第一课的战斗并取胜，按游戏自己的帧率：菜单 60 fps，战斗则受它自身的限制是 30（战斗的每个 30 秒区间都是 29.7–30.0，帧时间 p95 约 38 ms），声音正常（FMOD，没有欠载），在本课结束时存了游戏自己的档，冷启动后「继续游戏」可用（提示进入下一课）；随后第二课（城市与地形）玩到了它的第二天。手机 8 GB 内存里 PSS 2.35 GB，从未被杀。以游戏应用的形式打包（[它的说明](dm/games/0100300012F2A000/README.md#android)）。问题：一场战斗之后回到菜单，GPU 可能仍停留在战斗中轻松帧让驱动选定的频率，于是菜单只有 30 fps（GPU 24 ms 对 13），直到一次触摸把频率抬起来：只在脚本输入下见过这种情况，脚本不发送触摸。每种战斗动画第一次出现时会构建管线（一次最多 0.8 s 的帧）。画面里没看出问题，所以没有与 Mac 对比。在 Samsung Galaxy Z Flip 7（Xclipse 950，三星驱动）上，同样的一段从新游戏开始：部队、地图和战斗场景都能画出来（另一个安卓移植版在 Xclipse 上既画不出部队也画不出地图），战斗的每个 30 秒区间都是 29.7–30.0 fps，菜单 60，战斗之后也是（GPU 5 ms），声音没有欠载，存档和冷启动后的「继续游戏」都正常，11 GB 里 PSS 2.9–3.2 GB。没在其他设备上试过 |
| SHIN MEGAMI TENSEI V: Vengeance 1.0.3 | Samsung Galaxy S25 Ultra | 游戏内（贡献者报告）：三田的存档 30 fps，`DM_UE_DYNRES_BUDGET=16.7` 时 60（[它的说明](dm/games/010069C01AB82000/README.md#frame-rate)）。没在项目的设备上跑过 |
| DARK SOULS: REMASTERED 1.0.0 | Samsung Galaxy Z Flip 7、Ayn Odin 2 | 游戏内：在 Galaxy Z Flip 7（Xclipse 950）上，通过 adb 从新游戏玩过首次运行的设置、捏人（名字用安卓的键盘输入）和开场进到不死院的牢房，走动并转动视角，游戏自己的 30 fps（每个 30 秒区间 28.0–30.1），PSS 1.8 GB；游戏那种持续存盘在冷启动后由「继续游戏」载入（[它的说明](dm/games/01004AB00A260000/README.md#android)）。用从 1.0.3 派生的 profile 从卡带本体 1.0.0 构建，1.0.3 的 60 fps 补丁只对 1.0.3 有效，所以它和 Switch 一样跑 30。问题：在 Z Flip 7 上，开场影片的声音走第二个输出，约 9% 的时间欠载（会爆音）；游戏自己的声音没有欠载，而在 Ayn Odin 2（Adreno 740）上，同样一条路线进牢房 30 fps，影片输出只在 10 次报告中有 1 次欠载。没被证实可玩：是实时动作游戏，所以它那一段（不死院到不死院恶魔）需要真人上手柄。游戏应用留在 Odin 2 上供人试玩。没在其他设备上试过 |
| Super Mario Bros. Wonder 1.2.1 | POCO X5 5G（Adreno 619） | 游戏内：渲染倍率 0.8 下大约是游戏 60 的一半 30 fps，在关卡里和世界地图上都是；开到 60 fps 以下时，「食人花游行」会软锁（softlock），除非打开临时对策 `DM_AUDIO_PACE=game`（[音频](docs/reference/audio.md#music-timed-sequences-on-a-device-below-the-games-frame-rate)）† |
| Assassin's Creed: The Rebel Collection 1.0.0 | OnePlus Pad 3、Moto Razr Plus 2023、Ayn Odin 2、Galaxy Z Flip 7 | 游戏内：《黑旗》开场在海上的暴风中可以操控，Switch 上的 30 fps：Pad 3 上 5 分钟里 30.0 fps（p95 41 ms，GPU 12 ms，PSS 1.4 GB），Razr Plus 上 29.7 和 28.9（它有 2–7% 的帧要 50–73 ms，每帧的绘制和通道数都约为两倍）。从新游戏起，在 adb 上跑脚本：标题、菜单和输入名字，然后让爱德华沿甲板走到舵轮并转动视角，两台都这么跑。船、船员、暴风雨、炮火和 HUD 都画了出来，没有红色日志。开场所作的那份存档在重启后两台都能载入。声音在播：游戏的 PCM 转储里有信号，但没人听过。没有走到接舵和开船（接舵提示随着甲板摇晃出现又消失），也没有手工玩过。在 Ayn Odin 2（Adreno 740）上，同样的开场每个 30 秒区间都是 30.0 fps，GPU 9.3 ms，PSS 1.4 GB，没有红色日志，冷启动后存档能载入。在 Galaxy Z Flip 7（Xclipse 950，BC 纹理在 CPU 上解码）上同样：每个区间 30.0 fps，GPU 13 ms，PSS 1.9 GB，没有红色日志或欠载，存档能载入，爱德华走到了舵轮所在的抬升甲板。《叛变》用这张卡带跑不起来：那里 1 号程序只有影片，它的游戏数据是要下载的、没有导出（当成测试打包过一次，在第一帧之前就崩了）（[它的说明](dm/games/010044700DEB0000/README.md#android)） |
| Blasphemous 2 1.0.1 | Samsung Galaxy S25 Edge、Ayn Odin 2 | 游戏内：在 S25 Edge（Adreno 830）上，通过 adb 从新游戏玩过开场动画、苏醒和它的胆汁瓶教学，到三座雕像的房间并取走那里的剑，60 fps（每个 30 秒区间 58.8–60.0），声音正常（无欠载），PSS 2.0 GB（[它的说明](dm/games/010040801A4C8000/README.md#android)）。用从 1.0.8 派生的 profile 从卡带的 1.0.1 构建。没被证实可玩：游戏只在祈祷点存档，而那里没走到，所以存档和「继续游戏」都还没测；这是实时平台动作游戏，它那一段（到无面者）需要真人上手柄。画面里没看出问题；有一条红色日志（一种高级混合模式被当作普通混合绘制），没有与 Mac 对比。在 Ayn Odin 2（Adreno 740）上同样如此，60 fps，游戏应用留在那里供人试玩。没在其他设备上试过 |
| Super Mario 3D World + Bowser's Fury 1.2.2 | POCO X5 5G | 菜单：《Bowser's Fury》能启动，颜色也画得对；玩到哪里没有记录，有一次启动停在黑色的加载画面 † |
| Batman: Arkham Asylum 1.0.0 | Ayn Odin 2 | 游戏内：在 Ayn Odin 2（Adreno 740）上，通过 adb 从新游戏（普通难度）玩过语言选择、警告、标题和开场动画，到第一次跟在 Joker 护卫后面走过重症监护区，游玩中 28.5–29.7 fps（游戏自己的 30），声音正常（一个 6 声道 `AudioOut` 加 `AudioRenderer`，一次欠载），PSS 1.4 GB；冷启动后「继续剧情」能载入自动存档。它是从 Batman: Arkham Trilogy 卡带（里面有三款游戏：用 `--title-id` 挑一款，[#373](https://github.com/enjoyerofslop/droidplay-core/pull/373)）用临时 profile 打的包，仓库里目前还没有它的 profile：Rocksteady 的虚幻引擎 3 跑在 NVN 上，它的包用游戏自己的 Oodle 读取；41,809 个着色器里翻译了 40,443 个，剩下 1,366 个没翻，游玩中有 12 条「没有已翻译的着色器」红色日志，画面里没看出缺东西。没被证实可玩：实时动作游戏，所以它那一段需要真人。同一张卡带上的 Arkham City 和 Arkham Knight 是没有游戏数据的空壳（它们的游戏是要下载的，没有导出）。没在其他设备上试过 |
| The Elder Scrolls V: Skyrim 1.1.404 | Samsung Galaxy S25 Edge | 游戏内：在 S25 Edge（Adreno 830）上，通过 adb 从新游戏玩过标题、主菜单、开场坐马车进海尔根、捏人（在 DroidPlay 的文本框里取名）和巨龙来袭，到玩家可以操控的最初几步，30 fps（游戏自己的帧率：69 个区间里有 64 个的帧时间中位数是 33.0–33.5 ms，启动和加载时最高到 39.6 ms），PSS 3.2 GB；两个音频渲染器都有输出，没有试听；游戏写出了捏人时的存档和一份自动存档。它的 23,133 个着色器都在它的 BSA 包里和 main 里，这个 profile 起能读到。问题：一条红色日志，开场加载时出现 8 次（一个像素着色器读取了未绑定的 uniform 槽位 11；画面里没看出缺东西），以及主菜单的「开始新游戏？」框被画成两行、各占一屏高（Mac 上一样）。没被证实可玩：实时动作游戏，所以它那一段需要真人；存档没有回载验过；没在其他设备上试过 |
| Danganronpa V3 Anniversary Edition 1.0.2 | POCO X5 5G | 菜单：能启动、播出开场影片、画面也能画出来，用的是临时 profile；没有玩下去 † |
| Donkey Kong Country Returns HD 1.0.0 | Samsung Galaxy S25 Edge、Ayn Odin 2 | 游戏内：在 S25 Edge（Adreno 830）上，通过 adb 从一份新存档玩过标题、菜单、开场影片和树屋进到 1-1 Jungle Hijinxs（跑、跳、受伤），60 fps（每个 30 秒区间 59.6–60.1），声音正常（无欠载），PSS 2.5 GB；冷启动后存档由「继续游戏」载入（[它的说明](dm/games/01009D901BC56000/README.md#android)）。用从 1.1.0（Unity 6）派生的 profile 从卡带本体 1.0.0（Unity 2022.3）构建；它的 16,718 个着色器全部翻译。开场影片曾在 S25 Edge 和 Ayn Odin 2 上卡在第 3,570 帧里的第 3,566 帧（118.8 s），直到 2026-11-12 修好；修好后在 Odin 2 上能播到结尾，游戏随后自己往下走（[影片](docs/reference/movies.md#android-an-h264-movie-stops-a-few-pictures-before-its-end)；S25 Edge 上还没跑过）。Odin 2（Adreno 740）跑 1-1 也是 60 fps，游戏应用留在那里供人试玩。没被证实可玩：实时平台动作游戏，所以它那一段（1-1 到关底）需要真人上手柄。没在其他设备上试过 |
| Pokémon Legends: Arceus 1.1.1 | OnePlus Pad 3、Samsung Galaxy Z Flip 7、Samsung Galaxy Z Fold 8、Google Pixel 9 Pro XL | 可玩 – 有较严重问题，走过起始海滩的捕捉教学并进入祝庆村：在 v0.8.2 时，从新游戏起通过 adb 手工玩过，覆盖两个 GPU 家族。在 OnePlus Pad 3（Adreno 830）上：语言选择、在文本框里输入名字、阿尔宙斯的开场和坠落起始海滩、拉苯博士和三只宝可梦、阿尔宙斯手机，以及用第三个精灵球抓到火球鼠；然后从游戏菜单存档，冷启动后「继续游戏」回到存档的位置。与 Switch 相同的 30 fps（32 分钟里中位数 29.9），声音在播（无欠载；没有试听），一条红色日志（一次没有设置深度目标的 depth-stencil 清除），没有崩溃或被杀，常驻 1.9 GB。在 Galaxy Z Flip 7（Xclipse 950）上：开场、拉苯博士的三只宝可梦全部抓到（火球鼠在石头后面，水水獭在池塘里，木木枭在崖上），存档、冷启动、「继续游戏」回到原野，然后是带拉苯博士、花花夫人和夜晚村庄的祝庆村，又在那里存了档；海滩和捕捉全程 30 fps（34.5 分钟里中位数 29.9，最差的 30 秒区间 28.8，含天冠山的远景），祝庆村 18–28 fps（21 分钟里中位数 24.4），同一条红色日志，没有崩溃或被杀，常驻 2.0 GB（[它的说明](dm/games/01001F5010DFA000/README.md)）。在 Mac 上载入 Flip 的存档，标题的海滩、继续之后面向天冠山的原野（亮度分位数相差在 3 以内）和夜晚的村庄，看起来和 Flip 上一致。让它止步于「有轻微问题」的问题：游戏的第一次战斗在离开祝庆村之后的早上，没有走到；天冠山和裂缝的远景在 Pad 3 上有一分钟左右只有 21–26 fps（GPU 一帧 18–25 ms，别处是 13–17；Flip 上 30 fps）；祝庆村在 Flip 上 18–28 fps（GPU 一帧 17–22 ms，但那里重放等待在途提交的时间是一帧的 3–4.5 倍，海滩上不到一倍）；在 Flip 上，靠近镜头的岩石出现类似等高线的条纹，而 Pad 3 和 Mac 上同一批岩石没有。用别人的存档（不计入档位），在 Pad 3 和 Galaxy Z Flip 7（Xclipse 950）上，各通过 adb 逐步玩了约 12 分钟：在天冠山高原和黑曜原野走动与骑乘、快速旅行、一场战斗和一次捕捉、背包与存档菜单，以及安卓上存的存档在冷启动后重新载入，30 fps（Pad 3：中位数 30.1，最差 30 秒区间 28.5；Flip：中位数 29.9，最差 21.8 出现在首次构建 248 条管线时，之后 28–30），同一条红色日志，没有崩溃。更早：在 Galaxy Z Fold 8（Adreno 840，用它的外屏）上，从新游戏手工玩过开场到在起始海滩行走，30 fps（18 分钟里中位数 29.9，没有 30 秒区间低于 90%），常驻 1.6 GB，没有被 Android 17 的内存上限杀掉。在修好之前，安卓上画面发白且没有影子，原因是顶点着色器未写入的输出起始值被当成 (0, 0, 0, 1)（[写入输出的未写分量在安卓上也以 (0, 0, 0, 1) 起始](docs/reference/shaders.md#unwritten-components-of-a-written-output-start-as-0-0-0-1-on-android-too)）；修好之后，Fold 8 上海滩的画面与 Mac 一致。在 Pixel 9 Pro XL（Mali-G715）上，同样的开场也是 30 fps，角色和宝可梦也画了出来：游戏用 transform feedback 给它们蒙皮，在没有顶点阶段存储写入的 GPU 上，现在改为[在片元阶段捕获](docs/reference/rendering.md#transform-feedback-captured-in-the-fragment-stage-android)（通过起始海滩的对话验证）。构建时用手机解码游戏的 Oodle 包（[#320](https://github.com/enjoyerofslop/droidplay-core/pull/320)） |
| Pokémon Legends: Z-A 2.0.2 | Ayn Odin 2、Google Pixel 9 Pro XL | 游戏内：在 Ayn Odin 2（Adreno 740）上，通过 adb 从新游戏玩过语言、捏人和开场，到在密阿雷车站站台上游玩，30 fps（30 秒区间内 27.2–30.4），声音正常（无欠载），PSS 2.1 GB，画面与同一构建在 Mac 上的运行一致；用 R 存的存档在冷启动后由「继续游戏」载入（[它的说明](dm/games/0100F43008C44000/README.md#android)）。最初用从 2.0.2 派生的 profile 从卡带本体 1.0.0（Switch 1 版）构建（23,209 个着色器）；更新到 2.0.2 这个已注册的构建（28,603 个着色器，全部翻译）后同样跑通了：在 1.0.0 上存的存档能在它上面载入，每个 30 秒区间都是 30 fps，在 2.0.2 上存的存档在冷启动后由「继续游戏」载入。通过 DroidPlay 安装：它 2.49 GiB 的着色器装不进一个游戏应用。没被证实可玩：车站的检票口和第一场战斗没走到，而且战斗是实时的。在 Google Pixel 9 Pro XL（Mali-G715）上，两个版本的站台都被画得近乎全黑，20 fps（那里是「游戏内，受阻」）；它的内存峰值 1.9 GB，远低于 Android 17 的上限。没在其他设备上试过 |
| Xenoblade Chronicles 2 2.1.0 | Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7、Moto Razr Plus 2023 | 可玩 – 有较严重问题，走过阿伐利缇亚商会和第一次存档：在 Galaxy S25 Edge（Adreno 830）上，v0.8.2 时通过 adb 从新游戏（普通难度）手工玩过：开场（云海、打捞潜水、莱克斯和爷爷）、用自动攻击和「锚钩射击」战技赢下帝王蟹怪的教学战斗、其后的剧情、抵达阿伐利缇亚商会和那里的原野教学，以及在金口回港走动；然后 System → Save，冷启动后「继续游戏」回到同一处。开场和战斗与 Switch 相同是 30 fps（15.5 分钟里 29.9，最差 30 秒区间 28.9），声音在播（无欠载；没有试听），没有红色日志，没有崩溃或被杀，PSS 最高 3.3 GB（[它的说明](dm/games/0100E95004038000/README.md#android)）。让它止步于「有轻微问题」的问题：朝镇子里看时阿伐利缇亚只有 10–16 fps（一帧 2,200–2,800 次绘制，GPU 一帧 38–62 ms，别处约 20），朝码头外面看是 30，它那 6.5 分钟里平均约 20 fps；只玩了第一场战斗。角色和世界上很多地方（木箱、墙壁、爷爷的鳞片）上那层暗色点画与条纹——Mac 的画面上没有——自模板模式下的纹理槽位开始读取模板缓冲之后就消失了（已在 S25 Edge 和 Galaxy Z Flip 7 上确认，30 fps）。更早的时候，在任何手机上角色都画不出来，直到重放开始执行在光栅化丢弃下写内存的绘制（它的 GPU 蒙皮）；修好之后，Moto Razr Plus 2023（Adreno 730）也以稳定 30 fps 打完了帝王蟹怪的战斗，而在它之前，Galaxy Z Flip 7（Xclipse 950）已经能以 30 fps 打到帝王蟹怪。用卡带的 2.1.0（已注册）配一个只含着色器的派生 profile 构建，因为导出里没有 DLC；12,738 个着色器全部翻译。没在其他设备上试过 |
| The Binding of Isaac: Afterbirth+ 1.7.9b | POCO X5 5G | 能启动：用临时 profile 带着它的《忏悔》DLC 跑了起来，着色器在运行中编译并在手机上捕获；跑到哪里没有记录 † |
| Xenoblade Chronicles 3 1.0.0 | Ayn Odin 2、Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7、Moto Razr Plus 2023 | 可玩 – 有较严重问题，走过开场、最初的四场战斗和永烬平原直到存了一次档：在 Ayn Odin 2（Adreno 740，驱动 V@0676.0）上，用 `main` 在 3d9f479c 打的游戏应用，通过 adb 从新游戏（普通难度）手工玩过。覆盖了开场的过场、四场全部取胜的战斗（自动攻击、战技、一次角色行动和天赋战技），以及白天的平原朝向 9 号殖民地；然后 System → Save，冷启动后「继续游戏」回到同一处。与 Switch 相同的 30 fps，276 个十秒区间无一例外（680 MHz 下 GPU 11.5 ms），声音在播（无欠载；没有试听），没有崩溃或被杀，PSS 2.9–3.3 GB。Galaxy Z Flip 7（Xclipse 950）和 Moto Razr Plus 2023（Adreno 730）在 `main` 的 021fc6b6 上、带重放等待修复 #367–#369，跑完了同样的路线，含存档和「继续游戏」。Z Flip 7 在 294 个区间中的 280 个保持 30 fps（GPU 18.6 ms）；Razr 的过场是 30 fps，但战斗和平原是 17–28 fps，受它自身的 GPU 限制。在 Galaxy S25 Edge（Adreno 830）上，开场、第一场战斗和平原都是 30 fps（GPU 24.6–24.9 ms）；在 #367–#369 之前，它的游玩只有 5.6–7 fps。让它止步于「有轻微问题」的问题：每次会话一条红色日志（一个没有捕获变体的 transform-feedback 顶点着色器，它的效果没被找到）；存档位的缩略图是黑的；只在第一场战斗里与 Mac 对比过画面；白天平原上 Z Flip 7 的 GPU 忙到 85–95%，有些区间掉到 23–28 fps；Razr 的战斗 17–28 fps（[它的说明](dm/games/010074F013262000/README.md#android)）。用从 2.2.1 派生的 profile 从卡带本体 1.0.0 构建；它的 26,907 个着色器全部翻译。没试：平原之后、其他设备 |
| Metroid Dread 1.0.0 | Google Pixel 9 Pro XL、Moto Razr Plus 2023、Retroid Pocket 5 | 游戏内：在 Pixel 9 Pro XL（Mali-G715）、Razr Plus 2023（Adreno 730）和 Retroid Pocket 5（Adreno 650）上，通过 adb 从新游戏玩过开场影片、简报和母舰接近，到在第一个洞窟里可以操控，然后走过后面几个洞窟、行走跳跃射击，并与那里的爬行虫打了一场。Pixel 上 60 fps（GPU 9–10 ms，最高 2.6 GB），Razr 上 52–60（洞窟里 52–53，PSS 2.5 GB），Retroid Pocket 5 上 53–58（PSS 2.6 GB）。第一个房间看起来与 Mac 一致；一条红色日志（一次没有深度目标的 depth-stencil 清除）；Pixel 上 152 次报告里有 2 次短暂欠载，另两台没有。用从 2.1.0 派生的 profile 打包（卡带里装的是 1.0.0）。没试：存档（没走到存档站）、第一个洞窟之后、真人游玩（[它的说明](dm/games/010093801237C000/README.md#android)） |
| Metroid Prime Remastered 1.0.0 | Moto Razr Plus 2023、Google Pixel 9 Pro XL | 游戏内：在 Razr Plus 2023（Adreno 730）上，通过 adb 从新游戏开始（菜单用按帧计的按键操作）玩过简报和炮艇接近，到在奥尔菲恩号护卫舰的降落甲板上可以操控，走到锁定教学，60 fps（GPU 10 ms），PSS 2.0 GB，除了虚拟池重映射之外没有红色日志。问题：力场被画成一堆乱蓝形状，而不是半透明的青色板，臂炮是暗的。对游戏应用来说太大（2.66 GiB 的着色器），所以通过 DroidPlay 安装。在访客块按 32 MB 对齐之前，它在安卓上一启动就崩。在 Pixel 9 Pro XL（Mali-G715）上，标题画面近乎全黑，而且驱动在约 3 分钟后构建管线时崩溃。没试：声音、存档、第一个房间之后（[它的说明](dm/games/010012101468C000/README.md#android)） |
| **Mario Kart World 1.8.0（Switch 2）** | OnePlus Pad 3、装了 Turnip T30 驱动的 Galaxy S25 Edge、Google Pixel 9 Pro XL、Ayn Odin 2 | **游戏内，受阻**（2026-11-11，OnePlus Pad 3 加高通自家驱动）：标题、用 adb 输入操作的菜单，以及马力欧兄弟赛道的一场蘑菇杯比赛，能开能转向，比赛中 20–26 fps（一帧 34–50 ms；重放的 CPU 占 23–38 ms，GPU 18–29 ms），用的是它 profile 打开的 raw global memory，关掉这项时 15–22 fps，菜单约 30 fps；赛道没有贴图（稀疏纹理），路边没有灌木（没有网格着色器）。Galaxy S25 Edge 通过 `DM_VK_DRIVER` 用 Mr. Purple 的 Turnip T30 跑到了同一场比赛。它有 168 个计算着色器声明了 48 KB 共享内存，超过高通驱动接受的 32 KB：现在它们在那里改从 storage buffer 取；没有这项的话，GPU 在标题之后约 10 秒就丢了。菜单和比赛里偶发的故障（Pad 3 上是高通驱动里，S25 Edge 上是重放里，Google Pixel 9 Pro XL 上是 Mali 驱动里）来自一次被拒绝的虚拟池映射在池的预留区间里留下的空洞，已由 [#298](https://github.com/enjoyerofslop/droidplay-core/pull/298) 修好：修好之后，Pixel 9 Pro XL 走完菜单并在 4 次运行中 4 次跑完一场比赛（之前 4 次全失败），比赛中约 10 fps（一帧 97–99 ms，GPU 45 ms），S25 Edge 又跑了两场没有出故障。Odin 2（2026-11-08）：世界地图约 55 fps，演示行驶约 3.4 fps。待解决：内存（比赛中 12 GB 的 Pad 3 只剩 0.5–0.7 GB；开 raw global memory 跑得更快的那些运行都被杀了）、稀疏纹理、虚拟内存池、没有网格着色器 |
| **The Legend of Zelda: Ocarina of Time v131072（Switch 2）** | Samsung Galaxy Z Fold 8、Samsung Galaxy S25 Edge、Samsung Galaxy Z Flip 7、Google Pixel 9 Pro XL、Ayn Odin 2、Moto Razr Plus 2023 | **游戏内，受阻：**帧率不到目标（60 fps）的一半。从一份 Mac 存档，科奇里森林、萨莉亚的剧情和神圣森林里疯狂擦洗者的战斗在 Adreno 830 和 840 上有光照并画了出来、没有被杀（Galaxy S25 Edge 3 次运行 3 次成功，Galaxy Z Fold 8 启动 5 次），13–18 fps：Fold 上科奇里森林和萨莉亚剧情的帧率中位数 15–17 fps，森林里约 20。Galaxy Z Flip 7（Xclipse 950）上有光照地画出，约 12 fps，最高 8.25 GB；Pixel 9 Pro XL（Mali）有光照，约 9 fps。在 Adreno 7xx 的老一些的高通驱动上（Odin 2 的 740 是 V@0676，Razr 的 730 是 V@0615），角色是暗的：驱动拒绝 raw global memory 所用的指针转换（`OpConvertUToPtr`）；740 配 Turnip T30 能有光照地画出，约 9 fps；改从描述符数组访问 raw global memory 能让着色器在那里构建成功，但那样游戏就装不进 Odin 2 的内存了，所以它的 profile 把这项关着。科奇里森林里发白、平坦的水面是没被绘出的地形块，它们的地图由游戏在生成纹理之前从 CPU 填入：自 [#315](https://github.com/enjoyerofslop/droidplay-core/pull/315) 起能画出来（已在 Galaxy Z Fold 8 上确认）。待解决：帧率（CPU 的提交，每次绘制约 20 µs）、网格着色器渲染的植被没画出来（Vulkan 上还没有网格阶段），以及首次启动构建管线时约 10 秒的停顿 |

† 在 DroidPlay Core 并入 nxnative 的 `main`（2026-11-08）之前测的，之后没再跑过。带日期的「之后没再跑过」表示之后在某份代码上跑过、而 `main` 已经往前走了；“贡献者报告”表示是在贡献者自己设备上的运行。

前六款游戏、Final Fantasy Resonance 和 Breath of the Wild 的行来自 [安卓基线](dm/android/baselines.md)：在每台设备上跑的同一批脚本，含帧时间、设备所用的驱动，以及已知问题与其已知成因。最初一批是 2026-11-08 在 Odin 2、Pad 3 和 Retroid Pocket 5 上测的。2026-11-10 加上了 Galaxy S25 Edge 那一列，以及 Final Fantasy Resonance 和 Breath of the Wild 的行，Retroid Pocket 5 的行也重新测过；Galaxy Z Fold 8 上的 Ocarina of Time 和 Pixel 9 Pro XL 上的 Super Mario Odyssey 在那里各有自己的小节；之后重新测过的格子标了日期（Smash 的战斗、Link's Awakening 的远古遗迹、Skyward Sword HD 的天空阁）。其余的行来自各游戏自己的说明（[游戏表](dm/games/README.md#games)有链接），只有两个例外：SHIN MEGAMI TENSEI V: Vengeance 的设备是在其贡献者的 pull request 里点明的（[#101](https://github.com/enjoyerofslop/droidplay-core/pull/101)），而 POCO X5 5G 的那几行来自最初那版移植的 README。

[游戏表](dm/games/README.md#games)里其他每一款游戏都有 profile，也能用同样的方式打包，只是还没在安卓上跑过。没有 profile 的游戏仍然可以打成*实验性构建*：很可能起不来，但它是移植这款游戏的起点。

安卓宿主机只重放 NVN。用 OpenGL 绘制的游戏，或者自己发 Vulkan 调用的游戏（在游戏表的 Graphics 一列里写着 OpenGL 或 Vulkan），在安卓上画不出来，因为 OpenGL 和 Vulkan 这两层是 Mac 上的、基于 Metal：Balatro、Digimon Story Cyber Sleuth、Street Fighter 30th Anniversary Collection 和 Well Dweller（OpenGL），以及 Hades 和两款 Super Mario Galaxy（Vulkan）。打包脚本会在这类游戏上停下并说明原因，停在改写和着色器之前。Super Mario 3D All-Stars 仍能构建，因为它的启动器用 NVN 绘制，但里面的 Super Mario 64 和 Sunshine 调用 Vulkan，画不出来。被脚本拒绝的游戏属于「跑不起来」这一档。Street Fighter 30th Anniversary Collection 在脚本拒绝它之前，曾在 Retroid Pocket 5 上停在第一次 EGL 调用（[它的说明](dm/games/0100024008310000/README.md#android)）。

把着色器放在用游戏自己的 Oodle 压缩的包里的游戏，第一次构建时需要连着手机：Pokémon Legends: Arceus、Pokémon Legends: Z-A、Bayonetta 3、Batman: Arkham Knight 和 EA SPORTS FC 27。打包脚本在切分着色器之前，会用游戏自己的解码器在手机上解开这些包，这会多花几分钟，并把解出来的流（几个 GB）留在游戏的构建文件夹里供后续构建使用；如果你在 Mac 上用 DroidPlay for Mac 的构建跑同一款游戏，则由它的 Mac 宿主机来做。两者都没有时，脚本一开始就会停下并说明原因（[#310](https://github.com/enjoyerofslop/droidplay-core/issues/310)）。用这种方式构建的 Arceus 在 Galaxy Z Fold 8 上是「游戏内」（见上面它的游戏状态行）；其余几款还没在安卓上跑过。

## <a id="help-and-reports"></a>帮助与反馈

- **在 [DroidPlay Discord](https://discord.gg/3r92f8wmh7) 里问：**遇到问题去 #help，想知道某款游戏在自己设备上表现如何去 #compatibility。它的规矩和这份 README 一样：不许发游戏、密钥、固件或打包好的 APK。
- **构建失败时**，DroidPlay for Windows 会用大白话说清原因，有对应修复按钮的地方也会给出按钮。否则，用「构建」页面上的**复制报告**把一份简短报告复制下来贴到 #help；报告不会带上你的用户目录、手机序列号，以及任何看起来像密钥的东西。
- **一份有用的报告**会写明设备和它的 GPU（设置里能看到，或用 `adb shell getprop ro.product.model`）、安卓版本、游戏、它的 title ID 和版本、是怎么打包的（DroidPlay、命令行、游戏应用还是启动器），并附上日志：`adb logcat -s DroidPlay`（0.5.0 之前的应用用 `-s nxnative`），或者应用文件夹里的 `log.txt`（`Android/data/<package>/files/`）。一张截图加上日志里最前面的几行 `[RED]` 最有帮助。绝不要附上游戏文件或密钥。
- **测试者和贡献者**还可以用缺陷报告表单开 issue（[报告问题](CONTRIBUTING.md#reporting-a-problem)）。

## <a id="guides"></a>指南

- [DroidPlay for Windows](docs/android.md#droidplay-for-windows)：安装、开始使用，以及应用的每一个页面，都很详细。
- [安卓应用](docs/android.md#the-android-app)：启动器、单款游戏的设置、首次启动、操作、存档和日志。
- [游戏应用](docs/android.md#game-apps)：把一款游戏单独做成一个应用。
- [另一个 Vulkan 驱动（Turnip）](docs/android.md#another-vulkan-driver-turnip)：在 Adreno 或 Xclipse GPU 上，使用你装到手机上的驱动。
- [运行时才编译着色器的游戏](docs/android.md#games-that-compile-their-shaders-while-they-run)：比如 The Binding of Isaac。
- [用命令行打包](docs/android.md#packing-from-the-command-line)：需要什么，以及有哪些选项。
- [看清游戏到底画了什么](docs/android.md#seeing-what-a-game-draws)：从运行中的游戏截屏、导出帧、看线程状态。

## <a id="how-it-works"></a>工作原理

Switch 和安卓手机运行的都是 ARM64 代码，所以不需要模拟 CPU。游戏的代码只在宿主机需要的地方被改写（系统调用、线程寄存器），由一个宿主机来应答 Switch 的系统调用和 SDK 服务，游戏的 NVN 图形则通过 Vulkan 在 GPU 上重放，它的着色器在构建游戏时被翻译成 SPIR-V。

### 各部分怎么拼在一起

```
 你的电脑（Windows、macOS 或 Linux）                      你的安卓手机
 ───────────────────────────────────────────────────────  ─────────────────────────────────────────────────────────
 NSP / XCI 文件 + prod.keys                               DroidPlay 应用（org.nxnative.android）
          │                                               ├─ 启动器：手机上的游戏、
          ▼                                               │    每款游戏的设置、开始游戏
 桌面应用：scripts/nxnative_android.py                    │
 （或者命令行：scripts/build_android_from_nsp.py）        └─ 游戏画面，在自己的进程里：
          │  1. 解开游戏（nx_extract）                       载入那款游戏的宿主机
          │  2. 为安卓改写它的代码（patch_nso.py）           （libdmhost_<title ID>.so），由它运行
          │  3. 切分它的着色器，翻译成 SPIR-V                游戏的代码并在 Vulkan 上重放
          │  4. 用 Android NDK 构建这款游戏的宿主机          它的图形
          │  5. 打一个 APK，装上目前构建过的每一款游戏
          └─ adb：安装 APK，复制游戏文件 ──────▶          Android/data/org.nxnative.android/files/games/<title ID>/
```

一个应用装下所有游戏：你每构建一款游戏，它的宿主机就被加到电脑上的一个库中，而每个 APK 都是用整个库打的包，所以构建第二款游戏时第一款仍留在应用里。游戏文件（代码、着色器、RomFS、图标）放在手机上的应用文件夹里；存档留在应用的内部存储里。

### 安卓移植改了什么

iOS / Mac 的宿主机跑在安卓上，靠替代实现顶替它调用的 Darwin 接口（`dm/android/compat`）；访客的线程槽通过 x18 寄存器（`DM_TARGET=android` 时，改写器会生成 `mov xN, x18`）。NVN 在 Vulkan 上重放（`dm/android/gfx_vk.c`、`gfx_vk_draw.inc`）：纹理（GPU 不支持时在 CPU 上解 BC）、拷贝、清除、绘制、计算、间接绘制、transform feedback、查询和时间戳，分块提交，让 GPU 干活的同时 CPU 继续录制；着色器用项目自己的翻译器翻译，并针对安卓驱动做调整（`dm/android/tools/spv_android.py`）。音频走 AAudio，影片走 MediaCodec。移植的细节见：[dm/android/README.md](dm/android/README.md)。

一路上发现的问题，每一处的原因和修法都在参考文档里（[渲染](docs/reference/rendering.md#android-vulkan-replay)、[内存](docs/reference/memory.md)、[NVN 对象](docs/reference/nvn-objects.md)）：

- **画面不对**：Adreno 驱动把 uniform buffer 里的动态向量分量读错（竖条）；渲染目标按 sRGB 视图格式挂上（颜色发白）；安卓上 `char` 是无符号的（云里有噪点）；纹理和采样器 bank 被打包进同一个字段，导致分别读取时被当成「没有纹理」（《弹丸论破 V3》的黑屏）；第二个 NVN 设备重置了窗口原点（画面上下颠倒）；一张 3D 调色 LUT 一片一片地被画进同一片上（《Bowser's Fury》的蓝色场景）。
- **崩溃**：线程栈按 bionic 的保护页上报，Unity 的垃圾回收器扫描到了它（《弹丸论破 V3》启动时）；在游戏线程的小栈上执行 `pthread_exit`（《Bowser's Fury》过几秒后）。
- **速度**：同步只限在一次绘制所读的范围、保持渲染通道开着、通道早期与中途提交、常量缓冲只拷到着色器读到的位置、用状态字段构建管线键、限制管线预构建；*游戏时间*模式把音频对齐到游戏的帧，用于那些按音乐计时的关卡。

## <a id="contributing"></a>参与贡献

DroidPlay Core 就是带安卓移植的 nxnative。安卓相关的工作放在这里；针对 Mac 或 iPhone 的修复先提交到 [seedds/nxnative](https://github.com/seedds/nxnative)，再随下一次合并进入 DroidPlay Core。nxnative 的 `main` 会定期合进来，所以它的游戏、修复和 Switch 2 相关工作也会来到安卓；nxnative 本身按其维护者的选择保持只支持苹果平台。欢迎测试者和贡献者。

- [CONTRIBUTING.md](CONTRIBUTING.md#droidplay-core)：改动怎么进入、要跑哪些检查，以及 DroidPlay Core 如何与 nxnative 保持一致。
- [dm/android/README.md](dm/android/README.md)：安卓宿主机、Vulkan 重放、打包、游戏应用和桌面应用。
- [安卓基线](dm/android/baselines.md)：在每台设备上跑的同一批脚本，含帧时间、驱动和已知问题。
- [游戏表](dm/games/README.md#games) 以及每款游戏的说明：它的 profile 需要什么、在上面发现了什么、还有什么没解决。
- [AGENTS.md](AGENTS.md) 和 [docs/agents](docs/agents/README.md)：遇到崩溃、卡死或画面不对时从哪里入手。
- [docs/development.md](docs/development.md)：nxnative 的内部结构、打包脚本的选项，以及手工构建。

## <a id="credits-and-license"></a>致谢与许可

- [seedds/nxnative](https://github.com/seedds/nxnative) 让 Switch 游戏在 iPhone、iPad 和 Mac 上原生运行；DroidPlay Core 就是它加上安卓移植。下面 nxnative 的[致谢](#acknowledgements)列出了两者共同依赖的工作。
- [RogelioLB/nxnative-android](https://github.com/RogelioLB/nxnative-android) 开启了这次移植：NVN 的 Vulkan 重放、安卓前端和打包脚本。
- DroidPlay Core 在 2026-11-09 之前叫 droidnative，改名是为了不与 [DroidNative](https://github.com/DroidNative/DroidNativeApp) 混淆——后者是在安卓上运行 Linux 桌面应用（[#40](https://github.com/enjoyerofslop/droidplay-core/issues/40)）。指向旧名字的链接都会到这里。
- MIT（[LICENSE](LICENSE)）。第三方代码保留各自的许可（[dm/third_party](dm/third_party/README.md)）。

下面这条线以下是 nxnative 自己的 README，随它的其他改动一起合并进来：为 iPhone、iPad 和 Mac 构建游戏。

---

# nxnative

在你自己的 Apple 芯片 Mac、iPhone 和 iPad 上原生玩你自己的 Nintendo Switch 和 Switch 2 游戏。一个脚本就能把你的游戏打包成一个 Mac 应用，或者一个未签名的、由你自己侧载的 IPA。

它不是模拟器：游戏自己的代码直接跑在 Apple 芯片上，Switch 的图形在 Metal 上重建。本仓库不含任何游戏内容，本项目与任天堂及任何游戏发行商均无关联。

[游戏](#games) · [社区前端](#community-front-ends) · [环境要求](#requirements) · [怎么玩](#how-to-play) · [讨论](#discussions) · [给开发者](#for-developers)

## <a id="games"></a>游戏

完整的[已测试游戏表](dm/games/README.md#games)收录了 Switch 原生游戏、已测试的构建、引擎和图形 API。每款游戏的说明记录了它测试过的平台、进度和已知问题。

下面这些 Switch 2 游戏已通过 Mac 上的游玩测试。它们可用[`.nup` 文件或导出目录](#switch-2-games)构建：

- [Donkey Kong Bananza](dm/games/040074A01BF12000/README.md)
- [Fire Emblem Fortune's Weave](dm/games/04007EF01F8AE000/README.md) —— 最高可达 120 fps
- [Hyrule Warriors: Age of Imprisonment](dm/games/04003F40232DE000/README.md)
- [Kirby Air Riders](dm/games/040077201BE50000/README.md)
- [Mario Kart World](dm/games/0400C3F00006E000/README.md)
- [Mario Tennis Fever](dm/games/0400D4201C6EA000/README.md)
- [Pokémon Pokopia](dm/games/0400A3A01EE4C000/README.md)
- [Splatoon Raiders](dm/games/0400380020056000/README.md)
- [Star Fox](dm/games/0400E88025B1A000/README.md)
- [The Legend of Zelda: Ocarina of Time](dm/games/0400486024DEC000/README.md)
- [Yoshi and the Mysterious Book](dm/games/0400245021D2C000/README.md)

## <a id="community-front-ends"></a>社区前端

社区项目在 nxnative 之上加了工具，让你不用命令行就能把游戏变成 iPhone、iPad 或 Mac 上的应用，还有一些用来整理和启动游戏的库。它们是各自独立的项目：相关的问题和 bug 请到它们自己的页面反馈。

- [NX2Apple](https://github.com/LNPANDY/NX2Apple) —— Mac 上的构建器，带 iPhone/iPad 共享游戏库。
- [NX Play](https://github.com/varyform/nx-native-wrapper) —— Mac 上的游戏库，可安装到设备并同步存档。
- [NxNative Launcher](https://github.com/rennan101/nxnative_Launcher) —— Mac 启动器，带引导式构建和手柄映射。
- [LumaNX](https://github.com/Xc1Ym/LumaNX) —— Mac 游戏构建器，可导出 IPA。
- [GameCase](https://github.com/Tiaoge-tou/GameCase) —— 基于 LiveContainer 的 iOS 游戏库。

## <a id="requirements"></a>环境要求

- **Mac：**Apple 芯片，macOS 26.6 或更高版本。构建游戏需要 Xcode 27.2。
- **iPhone：**A17 Pro 芯片或更新的，iOS 26 或更高版本。
- **iPad：**M1 芯片或更新的，iPadOS 26 或更高版本。

游戏的纹理是 BC 压缩的，较老的 iPhone 读不了。Switch 2 的构建在 Mac 上测试；具体设备上的验证请见各游戏的说明。

对于没有 profile 的游戏，脚本会写一份勘察报告，并用猜出来的设置尝试一次临时构建。那次构建可能起不来；见[移植另一款游戏](docs/development.md#port-another-game)。

## <a id="how-to-play"></a>怎么玩

Switch 2 游戏是从一个 `.nup` 文件或它的一个文件目录构建的，不用 NSP，也不需要 `prod.keys`：见 [Switch 2 游戏](#switch-2-games)。在安卓上它们还处在早期阶段（[游戏状态](#game-status)）；在 DroidPlay for Windows 里，**+ 构建游戏**会让你选放着 `.nup` 或导出文件的那个文件夹。

### <a id="build-from-the-command-line"></a>用命令行构建

你需要一台 macOS 26.6 或更高版本的 Mac、[Xcode](https://developer.apple.com/download/all/?q=Xcode%2027.2) 27.2、[Homebrew](https://brew.sh) 和 Python 3.12 或更高版本（要 arm64 的，不能用 Intel 版 Homebrew 装的）。要构建到 iPhone，还需要 Xcode 的 iOS 平台（Xcode → Settings → Components）。

着色器用 Xcode 27.2 的 Metal 编译器构建。在第 1 步之前先选中它：`sudo xcode-select -s /Applications/Xcode.app`。装了多个 Xcode 版本时，把这个命名为 `Xcode-27.2.app`，再用 `sudo xcode-select -s /Applications/Xcode-27.2.app` 选中它。

**1. 安装工具**（只需一次），在「终端」里：

```
xcodebuild -downloadComponent MetalToolchain
git clone https://github.com/seedds/nxnative.git && cd nxnative
brew install xcodegen zstd glslang
brew install --cask dotnet-sdk
python3 -m pip install lz4 "capstone>=5,<6" fonttools nsz zbic "backports.zstd; python_version < '3.14'"
```

**2. 把游戏放进一个文件夹**：本体，以及你有的更新和 DLC（`.nsp`、`.xci`、`.nsz` 或 `.xcz`）：

```
~/Games/MarioWonder/
  Super Mario Bros. Wonder [010015100B514000][v0].nsp
  Super Mario Bros. Wonder [010015100B514800][v327680].nsp
```

**3. 构建**，给出游戏文件夹和你的 `prod.keys`：

```
python3 scripts/build_ipa_from_nsp.py ~/Games/MarioWonder -k ~/keys/prod.keys
```

IPA 会出现在游戏文件夹里。第一次构建要 30–60 分钟，需要约两倍游戏体积加 10 GB 的可用磁盘空间；再次构建会快得多。

想在 Mac 上玩的话，加上 `--platform mac-app`：你会得到一个可以从「访达」里打开的 Mac 应用。全部选项见：[打包脚本详解](docs/development.md#the-packing-script-in-detail)。

**安卓。** 想在安卓手机上玩，见[本页开头](#droidplay-core)：由桌面应用打包游戏并装到手机上。

### <a id="install"></a>安装

用 AltStore、Sideloadly 或 LiveContainer 这类侧载工具把 IPA 装到你的 iPhone 或 iPad 上。如果你的工具提供**Increased Memory Limit**（提高内存上限），把它打开：大一些的游戏需要它。

游戏太大装不进去？加上 `--romfs separate` 重新构建，并把脚本打印出的那条命令执行一次，把游戏文件复制到手机上（[快速重装](docs/development.md#quick-reinstalls)）。用 AltServer 的话，再加 `--shader-files`：它装不了 2 GiB 及以上的文件。

操作、存档和设置：[游玩](docs/playing.md)。

### <a id="switch-2-games"></a>Switch 2 游戏

Switch 2 游戏是从一个 [NUP](https://github.com/a55uka/nup) 容器（`.nup` 文件）或者它的一个文件目录构建的，不用 NSP。两者都不需要 `prod.keys`。项目还没有 profile 的游戏会被勘察并给出一个临时 profile，和 NSP 一样（[移植另一款游戏](docs/development.md#port-another-game)），它可能起不来。你得到的是 Mac 应用；iPhone 和 iPad 还没测试过。

**从一个 `.nup` 文件**，它把本体、更新和 DLC 装在一个文件里。给出这个文件，或者放着它的文件夹：

```
python3 scripts/build_ipa_from_nsp.py ~/Games/DonkeyKongBananza.nup --platform mac-app
```

[Hyrule Warriors: Age of Imprisonment](dm/games/04003F40232DE000/README.md) 就是这么玩起来的：它 47 GB 的 NUP 解包不到五分钟。如果 NUP 里带着游戏的控制数据（它的 NACP）和图标，应用就能拿到游戏的名字和图标；否则名字来自游戏的 profile，应用没有图标，除非你用 `--icon <image>`（Spyder 里的 `ICON`；任意尺寸的 JPEG 或 PNG）给它一个。

没有本体的 NUP 也能用：当它本体包是空的，或者根本没有本体、而更新标着 `standalone_update` 时，就把这个更新当作整个游戏，脚本也会说明这一点。之后如果游戏因为缺文件停住，说明这个更新里只有改动过的部分：请打一个带本体的 NUP。默认选最新的更新；`--package v<N>` 可以选容器里的另一个版本。这种容器里没有 `v0`（本体）可选。

**从一个文件目录**。脚本期望这样的结构（`updates` 和 `dlc` 是可选的）：

```
~/Games/DonkeyKongBananza/
  base/exefs/                     main, main.npdm, sdk, rtld
  base/romfs/
  updates/458752/exefs/           更新的版本号，写十进制
  updates/458752/romfs/           打好补丁的 RomFS，不是补丁文件
  dlc/040074a01bf13001/0/romfs/   DLC 的 title ID
```

```
python3 scripts/build_ipa_from_nsp.py ~/Games/DonkeyKongBananza --platform mac-app
```

只放一个更新的文件夹也行（不要 `base/`），把 `exefs/` 和 `romfs/` 直接放在文件夹里也行，`nup extract` 写出来就是这样，它们会被当作 `base/`。应用没有图标，因为文件夹里没有；`--icon <image>`（Spyder 里的 `ICON`）可以给它一个。要把这样的文件夹变成 NUP：`nup pack ~/Games/DonkeyKongBananza game.nup`。

## <a id="discussions"></a>讨论

问题、某款游戏在你 Mac 或 iPhone 上跑得怎么样、以及各种想法，都发到 [Discussions](https://github.com/seedds/nxnative/discussions)；[Issues](https://github.com/seedds/nxnative/issues) 留给 bug，并附上日志。Ocarina of Time 的性能（帧率、分辨率、哪些 Mac 能稳住 60 fps）在 [Ocarina of Time: state on main](https://github.com/seedds/nxnative/discussions/1789) 里跟进。

## <a id="for-developers"></a>给开发者

[工作原理](docs/development.md) · [游戏说明](dm/games/README.md#games) · [起跑与调试](docs/agents/README.md) · [前端](docs/frontends.md) · [参与贡献](CONTRIBUTING.md)

## <a id="acknowledgements"></a>致谢

本项目建立在别人的工作之上（[许可证](dm/third_party/README.md)）：

- **[d2r-mobile](https://github.com/jhaizhou-ops/d2r-mobile)**（MIT）为《Diablo II: Resurrected》开创了这种原生执行的思路。nxnative 是从它的通用部分起步的：NSO 改写器、顶替 Horizon 的宿主机、NVN-on-Metal 层和 iOS 应用外壳。修复是双向流动的。
- **Ryujinx**（MIT）：它的着色器翻译器（`Ryujinx.Graphics.Shader`、`Ryujinx.Common` 和 `Spv.Generator` 1.3.2，位于 `dm/third_party/ryujinx`，几处修改列在[它的 README](dm/third_party/ryujinx/README.md) 里）把游戏的着色器变成 SPIR-V。它对内核和系统服务的模拟，在宿主机的行为存疑时也是一份参考。
- **[Atmosphère](https://github.com/Atmosphere-NX/Atmosphere)**：它的内核 mesosphère 是 Horizon 同步语义（地址仲裁器、条件变量）的参考实现。
- **[LibHac](https://github.com/Thealexbarney/LibHac)**：在 `dm/tools/nx_extract` 里读取 NSP，并把更新叠到本体之上。
- **[SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross)**：SPIR-V 转 Metal Shading Language。
- **[glslang](https://github.com/KhronosGroup/glslang)** 把 OpenGL 游戏的 GLSL 编译成 SPIR-V 供它使用。
- **[MacNativeGames](https://github.com/ly05010419/MacNativeGames)**（MIT）：`dm/gfx/nvn/nvn_mtl.m` 里 8 位索引的 GPU 扩展和通道内清除，以及着色器翻译器里可见性计数器的下沉。

## <a id="license"></a>许可

MIT（[LICENSE](LICENSE)）。第三方代码保留各自的许可（[dm/third_party](dm/third_party/README.md)）。
