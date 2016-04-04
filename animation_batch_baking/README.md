# Animation Batch Baking
## Description

This is an addon for Blender 2.76b. It is used for baking the entire set of animations of a Blender file.

The baking process makes the Blender file compatible with JME 3.

## Installation
Extract the .zip of this project or copy the code of the .py file. Paste the script in the folder (this is for Windows, C: partition, 64b systems) C:\Program Files\Blender Foundation\Blender\<Blender-version>\scripts\addons
You have to enable the addon via Add-ons entry in Blender User Preferences. Search by "Animation batch baking".

## Prerequisites
To have an active armature.
The armature has animations, but there is no active animations and the NLA stack is empty.
The animations follow an strict nomenclature (needed for my personal projects). The channel is specified in the action name: ActionName-channel_number

## Usage
In the NLA Editor, Edit menu, there will be a new entry called "Animation Batch Baking". Click on that entry when you are ready. The stored animation will be backed and saved under the same action names.

## Notes
Not fully optimised, so the baking process could be rather long (between 5 and 20 seconds in my models, it just dependes on the number and complexity of the actions).
v1.2 differs from v1.1 in the way channels group the actions to be baked. v1.2 no longer groups actions according to their number

## Version

1.2
