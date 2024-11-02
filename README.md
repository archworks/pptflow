# PPTFlow

## Overview

**PPTFlow** is a powerful desktop application that transforms PowerPoint presentations (PPT) into engaging videos with AI-generated voice narration. This tool is perfect for educators, marketers, and content creators looking to enhance their presentations and reach a wider audience.

## Features
- **Slide-to-Video Conversion**: Seamlessly convert PPT slides into engaging videos.
- **AI Voice Narration**: Generates high-quality voice narration based on the speaker notes, utilizing AI text-to-speech technology.
- **Subtitle Generation**: Automatically generate subtitles for improved accessibility.
- **Customizable Output**: Adjust narration speed, voice selection, and video quality based on your needs.
- **User-Friendly Interface**: Easy to navigate and set up, even for beginners.

## System Requirements
* Operating System
    * Windows: Windows 10 or later
    * macOS: macOS 10.15 (Catalina) or later
    * Linux: Most modern distributions (Ubuntu, Fedora, etc.)
* Hardware Requirements
    * RAM: Minimum of 4 GB (8 GB recommended for optimal performance)
    * Storage: At least 500 MB of free disk space
* Software Requirements
    * Microsoft PowerPoint (on Windows/macOS): Required for loading slides
    * LibreOffice (on Linux): Required for loading slides

## Installation Options
### 1. Installing the Released Application
For most users, the easiest way to get started is by downloading the pre-built application. Follow these steps:

1. **Download**: Visit our [Releases Page](https://github.com/archworks/pptflow/releases) and download the latest version for your operating system.
2. **Install**: Run the installer and follow the on-screen instructions.
3. **Launch**: Open the application from your desktop or start menu.

### 2. Running from Source Code
If you prefer to run the application directly from the source code, or if you want to contribute to the development, follow these steps:

#### Pre-Requisites

1. **Install Python**: Download and install Python 3.7 or later from its [official website](https://www.python.org/downloads/).
2. **Prepare Python Virtual Environment (optional but recommended)**: Open a terminal or command prompt and run.
    ```bash
    pip install virtualenv
    ``` 

#### Application Setup
1. **Clone the Repository**: Use git to clone the project repository, then navigate to the project directory.
    ```bash
    git clone https://github.com/archworks/pptflow.git
    cd pptflow
    ```
2. **Set Up a Virtual Environment (optional but recommended)**: Create a virtual environment to manage dependencies, then activate the virtual environment.
    * On Windows
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ``` 
    * On macOS/Linux
        ```bash
        python -m venv venv
        source venv/bin/activate
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
4. **Configure Parameters**: Copy the example environment configuration. Open the .env file in a text editor and customize the parameters as needed.
    ```bash
    cp .env.example .env
    ```
5. **Run the Application**: Launch the application by executing:
    ```bash
    python main.py
    ```    

## Usage Instructions

1. **Import PPT Slides**: Click on the "Import" button to load your PowerPoint presentation.
2. **Select Voice**: Choose from a variety of AI voices and languages for your narration.
3. **Customize Settings**: Adjust slide transitions, narration speed, and other settings as needed.
4. **Generate Video**: Once satisfied, click on the "Generate" button and choose your desired format and resolution.

## Frequently Asked Questions (FAQ)
### Q: How it works
A: PPTFlow utilizes the speaker notes from your PowerPoint slides to generate voice narration. When you import a PPT file, the application extracts the notes associated with each slide. The AI then constructs a voiceover that corresponds to these notes, allowing for a more informative and engaging presentation. This feature ensures that important details and context are conveyed effectively in the final video.

### Q: What file formats are supported for PPT slides?
A: PPTFlow supports PPT, PPTX.

### Q: Can I use my own voice instead of AI narration?
A: Currently, PPTFlow only supports AI-generated voices.

### Q: Is there a limit to the number of slides I can convert?
A: There is no hard limit; however, performance may vary based on the size of the presentation.

## Support

For support, please visit our [support page](#) or contact us at [support@example.com](mailto:support@example.com).

## License

This software is licensed under the [MIT License](LICENSE).

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## Acknowledgments

- Thank you to all the contributors and the open-source community for their support.
- Special thanks to the developers of the AI voice synthesis technology.

## Changelog

### Version 1.0.0
- Initial release with core features.
