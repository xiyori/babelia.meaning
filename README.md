# babelia.meaning
[Babel image archives](https://babelia.libraryofbabel.info/) meaning search tool built upon OpenCV framework.

The main idea is to select pixels with the same color from a babelia image. Then a line pattern can be automatically generated or manually drawn using the selected pixels as end points.

[![alt text](https://i.imgur.com/eaNz7NA.gif)](https://imgur.com/a/0tWv151)\
<sub>(GIF is clickable)</sub>

**Key features**

+ *Pattern generation with a [nearest point walk](https://en.wikipedia.org/wiki/Random_walk)*
+ *Manual drawing mode*
+ *Editable bookmark format to store your drawings*
+ *PNG image export (supports transparency)*
+ *Extensive settings to customize your experience*
+ *Comprehensive command manuals*

## Installation

To use this app you need to install Python first. Head over to [www.python.org](https://www.python.org/downloads/release/python-3810/) to download Python 3.8.10 installer.

*Notice. The app is tested for Python 3.8, but will probably work with later Python versions.*

Then run the command:

`pip install -r requirements.txt`

If you are using Anaconda, run the following commands:

`conda create --name babelia --file requirements_conda.txt`\
`conda activate babelia`\
`pip install -r requirements.txt`

Run the program by:

`python main.py`

## Getting started

First, download the desired image from the [babel image archives](https://babelia.libraryofbabel.info/) to the `data` folder. Run the app and input the image number or filename to open it:

```
user@MyPC:~/babelia.meaning$ python main.py

   0b - "example"
Use index or filename to access bookmark.

   0 - "babelia0.jpg"
Use index or filename to access image.
> 0
> babelia0
> babelia0.jpg
```

Move the mouse pointer in the opened window to generate some random patterns. Several pattern types are available through command options, for example, try:

```
> 0 --cos
> 0 -i
```

To display command manuals and guides use:

```
> help
> help open
```

Add `-d` option to the command to enter manual drawing mode :

```
> 0 -d
```

Then use the mouse to draw lines between selected points. Press `Z` to undo the last stroke, `Y` to redo, `D` to clear the canvas (no undo!), `Esc` to leave the editor.

To save the results close the editor window and run:

```
> bookmark my_drawing
```

Bookmark can be viewed by simply entering its index or name:

```
   0b - "example", 1b - "my_drawing"
Use index or filename to access bookmark.

   0 - "babelia0.jpg"
Use index or filename to access image.
> 1b
> my_drawing
```

Click anywhere in the window to edit the bookmark content.

To export a pattern or drawing to PNG run:

```
> export my_drawing
> export my_drawing_transparent -t
```

Leave the app by entering an empty command:

```
>

Program finished.
```

Have fun!

## TODO
+ Export animations to mp4/gif
+ Line eraser tool in drawing mode
