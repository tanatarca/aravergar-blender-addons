# Changelog for Animation Batch Baking

* **v1.0 [27-3-16]** - Fully functional script. Bakes all the actions of the model and store the result in actions with the same name.
* **v1.1 [31-3-16]** - Fixed a bug in which the script didn't bake the actions separately. Edited for compatibility with mounts.
* **v1.2 [4-4-16]** - Actions are baked on its own. The script no longer groups actions with the same name for baking. Instead, if there are any number of actions for the same animation (each for a different channel), they has to be groupped under the same action specifying the affected channels in the name (Animation-channel1,channel2_001)

## TODO

* Look for a way of integrating *Simplify Multiple F-Curves* within this script.

* Look for ways of exporting the result aside from the current savefile.
