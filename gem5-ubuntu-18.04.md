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
Add the following content in /etc/xinetd.d/rsh file


# default: on 
# descr and ption: The rshd server is the server for the rcmd(3) routine and, \ 
#    consequently, for the rsh(1) program. The server provides \ 
#    remote execution facilities with authentication based on \ 
#    privileged port numbers from trusted hosts. 
service shell 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rshd 
} 
 
/etc/xinetd.d/rlogin 
 
# default: on 
# descr and ption: rlogind is the server for the rlogin(1) program. The server \ 
#    provides a remote login facility with authentication based on \ 
#    privileged port numbers from trusted hosts. 
service login 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rlogind 
} 
 
/etc/xinetd.d/rexec 
 
# default: off 
# descr and ption: Rexecd is the server for the rexec(3) routine. The server \ 
#    provides remote execution facilities with authentication based \ 
#    on user names and passwords. 
service exec 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rexecd 
} 



## Umount the disk image
exit \
cd \
sudo umount /mnt/proc \
sudo umount /mnt/dev \
sudo umount /mnt
