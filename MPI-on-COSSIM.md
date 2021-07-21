#How to execute MPI on COSSIM?

## Mount the disk image through following commands
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt \
cd /mnt \
sudo mount --bind /proc /mnt/proc \
sudo mount --bind /dev /mnt/dev \
sudo chroot .

echo "nameserver 8.8.8.8" > /etc/resolv.conf

## Create the hosts file in Ubuntu 18.04 simulated image
You need to add the IP with the hostname for each gem5 node
```
vi /etc/hosts
```

## Create a .rhosts file in Ubuntu 18.04 simulated image
You need to create a .rhosts in the root home directory and write the hostnames of the hosts in order to access password-free
```
vi /root/.rhosts
```
