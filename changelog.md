# Changelog for Cyclic Animation Interpolation

* **v0.1 [25-2-16]** - Initial commit. The addon adds the next-to-last and second keyframes before and after the animation range. It does force Blender to interpolate the fcurve around the first and last keyframes.
* **v1.0 [25-2-16]** - Modified main body. Now the script removes the two newly inserted keyframes with fast mode enabled, so the fcurve doesn't reevaluate and the modified interpolation remains.
