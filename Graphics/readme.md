# Fur Project

The basis of this coursework is based around a fur model which is here constructed using a HairModel 
(which is simply an extension of BaseModel), which is fed vertex and normals information from a FurUtils
class. This class handles all of the changes requested by the control keys.

The fur is created by calculating coordinate startpoints and endpoints for each fur hair.
These coordinates are then paced to the hairmodel to render.
Each time a change tot he fur is made, the old fur model is removed from the scene and is replaced by a new
re-rendered model.

Other utility files (blender.py, shaders.py...) have been provided previously in workshops and have been used
to speed up writing of the code. Most of the work is performed in scene,main, furutils and hairmodel files.
A demo of the project working can be found in this directory under FurDemo.mkv

## How to run
1.Install requirements

```
pip install -r requirements.txt
```

2. Run main.py

```
python main.py
```

