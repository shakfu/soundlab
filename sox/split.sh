
rm -rf ./out

mkdir ./out

sox demo.wav out/.wav trim 0 30 : newfile : restart

