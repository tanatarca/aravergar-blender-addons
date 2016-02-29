# Cyclic Animation Interpolation
## Description

This is an addon for Blender 2.76. It is used for interpolating correctly the extremes of a cyclic animation.

Blender does not interpolates the beggining and end of an animation when we want it to make it cyclic. This addon solves this by forcing it to interpolate between the second and the second-to-last keyframes.

## Installation
Extract the .zip of this project or copy the code of the .py file. Paste the script in the folder (this is for Windows, C: partition, 64b systems) C:\Program Files\Blender Foundation\Blender\<Blender-version>\scripts\addons
You have to enable the addon via Add-ons entry in Blender User Preferences. Search by "Cyclic animation interpolation".

## Prerequisites
To have an active object.
This object has an animation. You intend it to be a cyclic or looping animation.
Therefore, the first and last keyframes sets have equal values.

## Usage
In the Graph Editor, Channel menu, there will be a new entry called "Interpolate Cyclic Animation". Click on that entry when you are ready and left-click on the Graph Editor main view (this is a bug I'll have to solve. The script should run without this click). All previously selected fcurves will be affected by this script. You'll note that, now, the fcurves evaluate so that it take into account keyframes beyond first and last recorded keyframes.

## Notes
I have used some junks of the code of Fabrizio Nunnari:
* [Simplify Multiple F-Curves](https://developer.blender.org/T36097) is a Blender addon to simplify and align the keyframes of multiple F-Curves at once.





