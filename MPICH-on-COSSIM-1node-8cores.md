# MPICH on COSSIM 1node 8cores

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

## 5. Umount the disk image
exit \
cd \
sudo umount /mnt/proc \
sudo umount /mnt/dev \
sudo umount /mnt

## 6. Start-up the GEM5 node
The following command will start the gem5 execution (you can see the statistics in folder $GEM5/node0):
```
$GEM5/build/ARM/gem5.opt -d $GEM5/node0 $GEM5/configs/example/arm/starter_fs.py --kernel=vmlinux.arm64 --num-cores=8 --disk-image=ubuntu-18.04-arm64-docker.img --script=/home/red-sea/COSSIM/cgem5/configs/boot/standAloneScript0.rcS
```
## 7. Open GEM5 terminal in order to interact with simulated OS
```
m5term 127.0.0.1 3456
```

## 8. Set the hostname and VEF environment
```
hostname node0
export PATH=$PATH:/opt/vef_prospector/bin/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/vef_prospector/lib/
```

## 9. Execute the MPI application from simulated environment
If you would like to execute the application with VEF traces replace the ```mpirun``` with ```vmpirun```.
```
mpirun -n 8 ./mpi_hello_world #execute the app
```

## 10. Execute vef_mixer and read traces (it should be used only after ```vmpirun```)
```
cd /mpi_hello_world-* #go to traces directory
vef_mixer -i VEFT.main -o output_trace.vef
cat output_trace.vef
```

## 11. Terminate the gem5
```
m5 exit
```
