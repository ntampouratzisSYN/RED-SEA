#Setup on Ubuntu 18.04
sudo apt update

#gem5 prerequisites
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev python3-dev python3-six python libboost-all-dev pkg-config

#certi prerequisites
sudo apt install cmake bison flex libxml2-dev

#omnet 5.0 prerequisites
sudo apt install openjdk-8-jdk openjdk-8-jre tcl-dev tk-dev qt4-qmake libqt4-dev libqt4-opengl-dev openmpi-bin libopenmpi-dev clang
