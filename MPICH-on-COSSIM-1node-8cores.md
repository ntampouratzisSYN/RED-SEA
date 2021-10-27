# Mount the Ubuntu 18.04 simulated image and configure the MPI environment

## 1. Mount the disk image
```
sudo mount -o loop,offset=65536 $HOME/COSSIM/kernels/disks/ubuntu-18.04-arm64-docker.img /mnt
cd /mnt
```
<b> To be noticed that the sudo code is: redsea1234 </b>

## 2. Copy the MPI application to Ubuntu 18.04 simulated image
```
sudo cp /home/red-sea/Desktop/mpi_hello_world.c .
```

## 3. Emulate the image through QEMU
```
sudo mount --bind /proc /mnt/proc
sudo mount --bind /dev /mnt/dev
sudo chroot .

echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

## 4. Compile the MPI application to Ubuntu 18.04 simulated image
```
mpicc -o mpi_hello_world mpi_hello_world.c
```
## 5. Execute the MPI application
```
mpirun -n 8 ./mpi_hello_world #execute the app
```
