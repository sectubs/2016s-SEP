rm -rf build
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig

cd ..

sudo cp ../Orcatun/tun_handler.py /usr/local/lib/python2.7/dist-packages/orcatun/tun_handler.py
sudo cp ../Orcatun/packet_handler.py /usr/local/lib/python2.7/dist-packages/orcatun/packet_handler.py
sudo cp ../Orcatun/ot.py /usr/local/lib/python2.7/dist-packages/orcatun/ot.py

echo
echo
echo "Achtung: Sicherstellen, dass 'swig' vorher installiert wurde"
echo "Dazu 'sudo apt-get install swig' ausführen" 
