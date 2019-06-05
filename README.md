# blener_io_earth_studio
Import Google Earth Studio scenes into Blender.

**Note: This addon only supports Blender 2.80.**

## Installation

Download the contents of the repository, and import the zip file as an addon into Blender.

## Usage

1. Export project data as a **JSON file**, with local coordinates (either with the render or separatedly).
Tracking points and local origin are supported.

2. Import the data into Blender through the import menu. This will import your tracking points and the camera path as 1:1 (1 Blender Unit = 1 meter)

3. The Blender scene is now synced to the Google Earth Studio render!

## Roadmap

- [x] Import camera animation and trackpoints
  - [ ] Add a scaling setting to scale the imported scene down
- [ ] Automatically add footage to scene if found
- [ ] Support for Global coordinates export (low priority)
