<div align="center">
<h1>PPTFlow</h1>
[English](../README.md) | **简体中文** <br>
<br>
</div>

**PPTFlow**是一款强大的桌面应用程序，分分钟将PPT演示文稿转换为专业视频，支持AI配音和字幕生成。可以帮助教育工作者、营销人员和内容创作者增强演示效果、扩大受众范围。

## 功能
- **开箱即用**：无需在线上传即可轻松将PPT幻灯片转换为视频
- **自然AI语音**：根据文字备注生成自然流畅的AI配音
- **字幕生成**：自动创建字幕以增强可读性
- **支持自定义**：根据个人偏好调整旁白速度、声音和视频质量

## 系统要求
* 操作系统和软件：
    * Windows：Win 10 或更高版本；微软PowerPoint、或金山WPS
    * macOS：10.15 (Catalina) 或更高版本；微软PowerPoint
    * Linux：主流发行版本；LibreOffice
* 硬件：
    * 内存：最低4GB
    * 存储：至少500MB磁盘空间

## 安装方式
### 1. 安装包方式
对于大多数用户来说，推荐直接下载构建好的安装包。请按照以下步骤：

1. **下载**：访问我们的[发布页面](https://github.com/archworks/pptflow/releases)并下载适用于您的操作系统的最新版本。
2. **安装**：运行安装程序并按照屏幕上的说明进行操作。
3. **启动**：从桌面或开始菜单打开应用程序。

### 2. 源代码方式
如果您想直接从源代码运行应用程序，请按照以下步骤：

#### 先决条件

1. **安装Python**：从[Pyton官网](https://www.python.org/downloads/)下载并安装Python3.9或更高版本。
2. **准备Python虚拟环境（推荐但非必须）**：打开终端或命令提示符并运行：
    ```bash
    pip install virtualenv
    ``` 
#### 应用程序设置
1. **克隆项目代码**：使用git克隆代码仓库
    ```bash
    git clone https://github.com/archworks/pptflow.git
    ```
    ```
    cd pptflow
    ```
2. **设置虚拟环境（推荐但非必须）**：创建虚拟环境以管理依赖项，然后激活虚拟环境。
    * Windows环境
        ```bash
        python -m venv .venv
        ```
        ```
        .venv\Scripts\activate.bat
        ``` 
    * macOS/Linux环境
        ```bash
        python -m venv .venv
        ```
        ```
        source .venv/bin/activate
        ``` 
3. **安装依赖项**
    * Windows环境
        ```bash
        pip install -r requirements_win.txt
        ```
    * macOS/Linux环境
        ```
        pip install -r requirements_unix.txt
        ```
4. **配置参数（推荐但非必须）**：复制示例环境配置。用文本编辑器打开 .env 文件并根据需要自定义参数。
    ```bash
    cp .env.example .env
    ```
5. **运行应用程序**：通过执行以下命令启动应用程序：
    ```bash
    python main.py
    ```    

## 操作步骤

1. **选择PPT文件**：点击“选择PPT”按钮，加载要转换的演示文稿。
2. **调整设置**：调整AI语音、旁白速度和其他设置。
3. **生成视频**：点击“生成视频”按钮，开始转换过程。
4. **预览和播放**：播放视频，确保一切内容看起来和听起来都符合预期。

## 常见问题解答 (FAQ)
### 问：它是如何工作的？
答：PPTFlow将PowerPoint演示文稿的每一张幻灯片转换为图像，提取演讲者备注以生成旁白和字幕，最后将所有内容合成视频。

### 问：PPTFlow 支持哪些文件格式的 PPT 幻灯片？
答：目前PPTFlow仅支持PPTX。

### 问：我可以使用自己的声音代替AI旁白吗？
答：目前PPTFlow仅支持AI生成的语音。

### 问：我可以转换的幻灯片数量有限制吗？
答：没有硬性限制；但幻灯片的数量将决定转换的速度。

## 技术支持

如需技术支持，请通过 [pptflow@archworks.tech](mailto:pptflow@archworsk.tech) 联系我们，访问我们的 Discord [频道](https://discord.gg/AKBXvyHCcv)，或添加 GitHub [问题](https://github.com/archworks/pptflow/issues)。

## 开源协议

本软件遵从 [Appache 2.0协议](LICENSE) 。

## 致谢

- 感谢所有贡献者和ArchWorks社区的支持。
- 特别感谢MoviePy、CustomTkinter等众多优秀开源项目的创建者和贡献者。