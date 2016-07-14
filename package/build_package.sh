#Orcatun - Ultrasonic Networking. Copyright (C) 2016 sectubs/2016s-SEP
cd orcatun_1.0-0
rm -r ./usr/share/orcatun
mkdir -p ./usr/share/orcatun
mkdir ./usr/share/orcatun/gr-orcatun
cp -r ../../Orcatun/* ./usr/share/orcatun/
cp -r ../../gr-orcatun/* ./usr/share/orcatun/gr-orcatun/
cd ..
dpkg-deb -b orcatun_1.0-0
