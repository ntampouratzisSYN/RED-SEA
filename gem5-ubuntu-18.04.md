# Ubuntu 18.04 disk image with RSH and MPI installed

## Download the ubuntu-18.04-arm64-docker.img.bz2 disk image from gem5 official repository: 
https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries \

## Mount the disk image through following commands
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt \
cd /mnt \
sudo mount --bind /proc /mnt/proc \
sudo mount --bind /dev /mnt/dev \
sudo chroot .

echo "nameserver 8.8.8.8" > /etc/resolv.conf


## Install the following packets
apt update \
apt install build-essential \
apt install net-tools \
apt install rsh-server \
apt install rsh-client \
apt install xinetd \
apt install vim \
apt install iputils-ping

## Install rsh under Ubuntu for passwordless access
Add the rsh file content in /etc/xinetd.d/rsh file

## Add the following line in gem5 script
/etc/init.d/xinetd restart 


## Umount the disk image
exit \
cd \
sudo umount /mnt/proc \
sudo umount /mnt/dev \
sudo umount /mnt
