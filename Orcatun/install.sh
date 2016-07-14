
echo "Create orcatun command"
sudo ln main.py -s -r -T /usr/bin/orcatun
sudo chmod 777 /usr/bin/orcatun
echo "Create gui command"
sudo ln gui-orcatun.py -s -r -T /usr/bin/orcagui
sudo chmod 777 /usr/bin/orcagui

echo "Create configuration"
sudo mkdir /etc/orcatun
sudo cp example.conf /etc/orcatun/orcatun.conf

echo "Set up manpage"
sudo cp orcatun.1.gz /usr/share/man/man1/orcatun.1.gz

echo "Build Orcatun"
cd ../gr-orcatun
sudo ./build.sh


echo "Finished"
