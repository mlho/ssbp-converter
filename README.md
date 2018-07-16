
# Convert and Assemble Sprite from .ssbp

## \*\* ONLY Supports SpriteStudio5 DATA_VERSION 3 .ssbp files \*\*


## Known Issues
- Vertex Transforms are not performed(can cause parts overlapping and incorrect sizing/positioning)
- Weapons and other Option parts/animations(Capes, Tails, Effects) are not drawn together


## Requirements
- [npm](https://nodejs.org/en/)
- [local http server](https://www.npmjs.com/package/http-server)
- [Python 3.6+](https://www.python.org/getit/)
- [Google Chrome](https://www.google.com/chrome/)
- [Inkscape](https://inkscape.org/en/) (Optional. Recommended for SVG manipulation)


## How To Use
1. Download and Extract .zip
2. Copy "convertSSBP.py" and "SpriteAssembler.html"
3. Navigate to the directory containing the .ssbp file and texture images
4. Paste "convertSSBP.py" and "SpriteAssembler.html"
5. Run "convertSSBP.py" from the directory containing the .ssbp file and textures, 5 JavaScript files should be generated

**Linux/Mac**
```
python convertSSBP.py [filename of .ssbp]
```
**Windows**
```
py convertSSBP.py [filename of .ssbp]
```

6. Run http-server from the same directory containing the .ssbp file and textures
7. Open "SpriteAssembler.html" at http://localhost:8080 in Google Chrome to view the output


## Not Implemented
- Label Data is not retrieved
- Effect Data is not retrieved
