
# Convert and Assemble Sprite from .ssbp

## \*\* ONLY Supports SpriteStudio5 DATA_VERSION 3 .ssbp files \*\*


## Known Issues
- Vertex Transforms are not performed(can cause parts overlapping and incorrect sizing/positioning)
- Weapons and other Option parts/animations(Capes, Tails, Effects) are not drawn together


## Requirements
- [local http server](https://www.npmjs.com/package/http-server)
- Python 3.6+
- Google Chrome
- Inkscape (Optional. Recommended for SVG manipulation)


## How To Use
- Download and Extract .zip
- Copy "convertSSBP.py" and "SpriteAssembler.html"
- Navigate to the directory containing the .ssbp file and texture images
- Paste "convertSSBP.py" and "SpriteAssembler.html"
- Run "convertSSBP.py" from the directory containing the .ssbp file and tex folder, 5 JavaScript files should be generated

**Linux/Mac**
```
python convertSSBP.py *[filename of .ssbp]*
```
**Windows**
```
py convertSSBP.py *[filename of .ssbp]*
```

- Run http-server from the same directory containing the .ssbp file and tex folder
- Open "SpriteAssembler.html" at http://localhost:8080 in Google Chrome to view the output


## Not Implemented
- Label Data is not retrieved
- Effect Data is not retrieved
