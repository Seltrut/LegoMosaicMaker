# LegoMosaicMaker
Create directions for mosaics made of lego from an input image

Currently the database included in the project has all of the current 1 x 1 dot pieces available from Lego's Pick A Brick tool.
If you want to use other 1 x 1 pieces you will have to run it with a different piece_id, like the following:
     flat dot pieces:      98138 
     dot pieces with hole: 85861
     classic style dots:   6141 (This is what is currently used)
You will also have to change line 52 in MosMaker.py to reflect this new piece id. (In the future I will be putting this variable in one place so only one change will be necessary)

To turn a picture into a lego mosaic add the image to ./pics/ and change the filename variable in MosMaker.py to the name of the picture you wish to use. 
LegoMosaicMaker currently will display your mosaic in 10 x 10 blocks which is the size of the lego panels that are used in similar products by Lego.
I'm currently working on adding these pictures to a pdf that will give explicit directions on how to create your lego mosaic in real life. A previous
iteration just output the Lego piece id for each piece in the mosaic one by one. This allowed me to use this to create mosaics but it was extremely 
tedious and I hope to avoid doing that again.
