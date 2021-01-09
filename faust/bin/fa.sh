
target=$1
name=`basename -s .dsp $1`
plugin=$name.component
lib=$HOME/Library/Audio/Plug-Ins/Components

faust2au $1
if [[ -e ./$plugin ]]; then
    cp -rf ./$plugin $lib/$plugin
    rm -rf $plugin
fi



