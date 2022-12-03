#!/bin/bash

# install dependencies
sudo apt install python3-pyaudio

# generate run script
touch ./run.sh
echo '#!/bin/bash' > run.sh
chmod u+x run.sh
echo "python3 $(pwd)/rng.py \"\$@\" 2> /dev/null" >> run.sh

# create symbolic link in /usr/local/bin
sudo ln -s $(pwd)/run.sh /usr/local/bin/mic-rng

echo "symbolic link created in /usr/local/bin"
echo "now run with mic-rng"
