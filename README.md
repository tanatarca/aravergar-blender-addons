# Cyclic Animation Interpolation
## A Python addon for Blender

This is an addon for Blender 2.76. It is used for interpolating correctly the extremes of a cyclic animation.

Blender does not interpolates the beggining and end of an animation when we want it to make it cyclic. This addon solves this by forcing it to interpolate between the second and the second-to-last keyframes.

I have used some junks of the code of Fabrizion Nunnari:
* ("Simplify Multiple F-Curves")[https://developer.blender.org/T36097] is a Blender addon to simplify and align the keyframes of multiple F-Curves at once.





