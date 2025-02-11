<div align="center">
<h1>PPTFlow</h1>

**English** | [简体中文](docs/README.zh.md) 
<br>
</div>


**PPTFlow** is a powerful desktop application that seamlessly transforms PowerPoint slides into engaging videos with AI-generated voiceover and subtitles. Perfect for educators, marketers, and content creators looking to enhance presentations and expand audience reach.

## Features
- **One-Click Conversion**: Effortlessly converts PPT slides into videos without the need for online uploads.
- **Natural AI Voice**: Generates natural-sounding AI voiceover from speaker notes.
- **Subtitle Generation**: Automatically creates subtitles for enhanced accessibility.
- **Customizable Output**: Adjust voiceover speed, voice, and video quality based on your needs.

## System Requirements
* Operating System and Software:
    * Windows: Win 10 or later; Microsoft PowerPoint
    * macOS: 10.15 (Catalina) or later; Microsoft PowerPoint
    * Linux: Most distros; LibreOffice 
* Hardware:
    * RAM: Minimum of 4 GB
    * Storage: At least 500 MB of free disk space
## Installation Options
### 1. Installing the Released Application
For most users, the easiest way to get started is by downloading the pre-built application. Follow these steps:

1. **Download**: Visit our [Releases Page](https://github.com/archworks/pptflow/releases) and download the latest version for your operating system.
2. **Install**: Run the installer and follow the on-screen instructions.
3. **Launch**: Open the application from your desktop or start menu.

### 2. Running from Source Code
If you prefer to run the application directly from the source code, follow these steps:

#### Pre-Requisites

1. **Install Python**: Download and install Python 3.9 or later from its [official website](https://www.python.org/downloads/).
2. **Prepare Python Virtual Environment (optional but recommended)**: Open a terminal or command prompt and run:
    ```bash
    pip install virtualenv
    ``` 
#### Application Setup
1. **Clone the Repository**: Use git to clone the project repository, then navigate to the project directory.
    ```bash
    git clone https://github.com/archworks/pptflow.git
    ```
    ```
    cd pptflow
    ```
2. **Set Up a Virtual Environment (optional but recommended)**: Create a virtual environment to manage dependencies, then activate the virtual environment.
    * On Windows
        ```bash
        python -m venv .venv
        ```
        ```
        .venv\Scripts\activate.bat
        ``` 
    * On macOS/Linux
        ```bash
        python -m venv .venv
        ```
        ```
        source .venv/bin/activate
        ``` 
3. **Install Dependencies**
    * On Windows
        ```bash
        pip install -r requirements_win.txt
        ```
    * On macOS/Linux  
        ```
        pip install -r requirements_unix.txt
        ```
4. **Configure Parameters (optional)**: Copy the example environment configuration. Open the .env file in a text editor and customize the parameters as needed.
    ```bash
    cp .env.example .env
    ```
5. **Run the Application**: Launch the application by executing:
    ```bash
    python main.py
    ```    

## Usage Instructions

1. **Select PowerPoint**: Click the ’Select PPT' button to load your PowerPoint presentation.
2. **Adjust Settings**: Adjust AI voice, voiceover speed, and other settings as needed.
3. **Generate Video**: Click on the "Generate Video" button to begin the conversion process.
4. **Preview and Play**: Play the video to ensure everything looks and sounds perfect.

## Frequently Asked Questions (FAQ)
### Q: How it works
A: PPTFlow converts each slide of a PowerPoint presentation into images, extracts speaker notes to generate voiceovers and subtitles, and finally compiles everything into a video.

### Q: What file formats are supported for PPT slides?
A: PPTFlow supports PPTX.

### Q: Can I use my own voice instead of AI voiceover?
A: Currently, PPTFlow only supports AI-generated voices.

### Q: Is there a limit to the number of slides I can convert?
A: There is no hard limit; however, performance may vary based on the size of the presentation.

## Support

For support, please contact us at [pptflow@archworks.tech](mailto:pptflow@archworsk.tech), visit our Discord [channel](https://discord.gg/AKBXvyHCcv), or add an Github [issue](https://github.com/archworks/pptflow/issues).

## License

This software is licensed under the [Appache 2.0 License](LICENSE).

## Acknowledgments

- Thanks to all the contributors and the ArchWorks community for their support.
- Special thanks to the creators and contributors of incredible open-source projects such as MoviePy, CustomTkinter, and many others.