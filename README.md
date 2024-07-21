### Requirements

<details>
<summary> Install prerequisites </summary> 
<div markdown="1">

## Windows:
    
Open Command Prompt as Administrator
    
- cd "C:\Program Files\Blender Foundation\Blender {Blender_version}\{Blender_version}\python\bin"
- python -m pip install --upgrade pip
- python -m pip install opencv-contrib-python numpy
- Blender Projector Add-on
    - https://github.com/Ocupe/Projectors
  
  </div>
  </details>
  

### Calibration

<details>
<summary> How to calibrate </summary> 
<div markdown="1">
        
    1. Run projector_setup_new.py
    2. Run register_calibr_poses.py  - capturing the location and rotation values of the calibration plane and storing them in an XML file
        1. locate calibration board
        2. press the "F" key to capture the pose.
        3. press the "ESC" key to save the poses in an extensible file (.xml).
    3. Run calibration.py

 </div>
  </details>
