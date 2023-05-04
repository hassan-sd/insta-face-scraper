
* Patreon: https://www.patreon.com/sd_hassan

# Insta Face Extractor

This is a Python script that allows you to extract faces from insta posts.

## Features

-   Downloads X amount of photos from X amount of instagram profiles
-   Extracts faces from the downloaded photos
-   Saves the extracted faces to disk separated by each person detected

## Installation

1.  Clone this repository or download the ZIP file and extract the contents.
2.  Install the required dependencies by running `pip install -r requirements.txt` in the root directory of the project.

## Usage

1.  Open a terminal or command prompt and navigate to the root directory of the project.
2.  Run the command `python hassan-insta.py` to launch the script.
3.  Enter the username of the instagram profile or else a file path to a text file that contains multiple usersnames, one per each line.
4.  The script will download the photos to the max amount you set and extract the faces. The extracted faces will be saved in the `faces` directory.


If you get a build error when installing requirements, you may need the Visual Studio Build tools c++ workload

Download build tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Then in the same folder where your EXE is, run this command:

`.\vs_BuildTools.exe --quiet --wait --norestart --nocache --installPath C:\BuildTools --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.Windows10SDK.19041`

or

`vs_BuildTools.exe --quiet --wait --norestart --nocache --installPath C:\BuildTools --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.Windows10SDK.19041`

Leave it running and you can see in your C:\BuildTools that new folders are being added. When it's finished, restart the PC and your package should install correctly 

## Video
https://user-images.githubusercontent.com/119671806/236062228-5513880d-7953-4a04-b79f-0a8725439175.mp4

