# DiffusionSifter
 Quickly sift through diffusion outputs

Currently hardcoded for my local filestructure but is simple enough to edit for yours.
Expects 4 folders containing diffusion outputs at 25, 50, 75 and 100 percent of the total steps.

Click the images or buttons or use hotkeys to sift through.

1,2,3,0 on numpad will pick the images at 100, 75, 50 or 25 steps respectively. 
Numpad . or Backspace will move an image to trash.
u will undo actions in reverse order. History is saved between sessions in a text file.

The process is lossless: images in the 100 folder are sorted into /processed or /trash to easily track progress but other folders are untouched and no files are deleted. 
