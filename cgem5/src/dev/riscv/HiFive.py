# Copyright (c) 2021 Huawei International
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.objects.Platform import Platform
from m5.objects.PMAChecker import PMAChecker
from m5.objects.Clint import Clint
from m5.objects.Plic import Plic
from m5.objects.RTC import RiscvRTC
from m5.objects.Uart import Uart8250
from m5.objects.Terminal import Terminal
from m5.params import *
from m5.proxy import *
from m5.util.fdthelper import *

from m5.objects.Ethernet import NSGigE, IGbE_igb, IGbE_e1000

from m5.objects.Device import BasicPioDevice
from m5.objects.PciHost import *
from m5.SimObject import SimObject

class GenericRiscvPciHost(GenericPciHost): #PCI
    type = 'GenericRiscvPciHost'
    cxx_header = "dev/riscv/pci_host.hh"
    int_base   = Param.Unsigned("PCI interrupt base")
    int_count  = Param.Unsigned("Maximum number of interrupts used by this host")
    
    # This python parameter can be used in configuration scripts to turn
    # on/off the fdt dma-coherent flag when doing dtb autogeneration
    _dma_coherent = True
    
    def generateDeviceTree(self, state):
        local_state = FdtState(
            addr_cells=3, size_cells=2,
            cpu_cells=1, interrupt_cells=1)

        node = FdtNode("pci")

        if int(self.conf_device_bits) == 8:
            node.appendCompatible("pci-host-cam-generic")
        elif int(self.conf_device_bits) == 12:
            node.appendCompatible("pci-host-ecam-generic")
        else:
            m5.fatal("No compatibility string for the set conf_device_width")

        node.append(FdtPropertyStrings("device_type", ["pci"]))

        # Cell sizes of child nodes/peripherals
        node.append(local_state.addrCellsProperty())
        node.append(local_state.sizeCellsProperty())
        node.append(local_state.interruptCellsProperty())
        # PCI address for CPU
        node.append(FdtPropertyWords("reg",
            state.addrCells(self.conf_base) +
            state.sizeCells(self.conf_size) ))

        # Ranges mapping
        # For now some of this is hard coded, because the PCI module does not
        # have a proper full understanding of the memory map, but adapting the
        # PCI module is beyond the scope of what I'm trying to do here.
        # Values are taken from the VExpress_GEM5_V1 platform.
        ranges = []
        # Pio address range
        ranges += self.pciFdtAddr(space=1, addr=0)
        ranges += state.addrCells(self.pci_pio_base)
        ranges += local_state.sizeCells(0x10000)  # Fixed size

        # AXI memory address range
        ranges += self.pciFdtAddr(space=2, addr=0)
        ranges += state.addrCells(self.pci_mem_base)
        ranges += local_state.sizeCells(0x40000000) # Fixed size
        node.append(FdtPropertyWords("ranges", ranges))

        if True:
            plic = self._parent.unproxy(self).plic
            int_phandle = state.phandle(plic)
            # Interrupt mapping
            interrupts = []

            # child interrupt specifier
            child_interrupt = local_state.interruptCells(0x0)

            # parent unit address
            parent_addr = 0x0                                               #get this from /gem5/system/arm/dt/platforms file

            for i in range(int(self.int_count)):
                parent_interrupt = int(self.int_base) + i                   #RISCV uses only 1 interrupt_cell in plic

                interrupts += self.pciFdtAddr(device=i, addr=0) + \
                    child_interrupt + [int_phandle] + [parent_addr] + \
                    [parent_interrupt]

            node.append(FdtPropertyWords("interrupt-map", interrupts))

            int_count = int(self.int_count)
            if int_count & (int_count - 1):
                fatal("PCI interrupt count should be power of 2")

            intmask = self.pciFdtAddr(device=int_count - 1, addr=0) + [0x0]
            node.append(FdtPropertyWords("interrupt-map-mask", intmask))
        else:
            m5.fatal("Unsupported PCI interrupt policy " +
                     "for Device Tree generation")

        if self._dma_coherent:
            node.append(FdtProperty("dma-coherent"))

        yield node


class HiFive(Platform):
    """HiFive Platform

    Implementation:
        This is the base class for SiFive's HiFive
        board series. It contains the CLINT and PLIC
        interrupt controllers, Uart and Disk.

        Implementation details are based on SiFive
        FU540-C000. https://sifive.cdn.prismic.io/
        sifive/b5e7a29c-d3c2-44ea-85fb-acc1df282e2
        1_FU540-C000-v1p3.pdf

    Setup:
        The following sections outline the required
        setup for a RISC-V HiFive platform. See
        configs/example/riscv/fs_linux.py for example.

    Driving CLINT:
        CLINT has an interrupt pin which increments
        mtime. It can be connected to any interrupt
        source pin which acts as the RTCCLK pin. An
        abstract RTC wrapper called RiscvRTC can be
        used.

    Attaching PLIC devices:
        PLIC handles external interrupts. Interrupt
        PioDevices should inherit from PlicIntDevice
        (PCI and DMA not yet implemented). It contains
        a parameter interrupt_id which should be used
        to call platform->postPciInt(id).

        All PLIC interrupt devices should be returned
        by _off_chip_devices(). Calling attachPlic sets
        up the PLIC interrupt source count.

    Uart:
        The HiFive platform also has an uart_int_id.
        This is because Uart8250 uses postConsoleInt
        instead of postPciInt. In the future if a Uart
        that inherits PlicIntDevice is implemented,
        this can be removed.

    Disk:
        See fs_linux.py for setup example.

    PMAChecker:
        The PMAChecker will be attached to the MMU of
        each CPU (which allows them to differ). See
        fs_linux.py for setup example.
    """
    type = 'HiFive'
    cxx_header = "dev/riscv/hifive.hh"
    system = Param.System(Parent.any, "system")

    # CLINT
    clint = Param.Clint(Clint(pio_addr=0x2000000), "CLINT")

    # PLIC
    plic = Param.Plic(Plic(pio_addr=0xc000000), "PLIC")
    
    #pci_host = GenericRiscvPciHost(                                                     #PCI
    #    conf_base=0x30000000, conf_size='256MiB', conf_device_bits=12,
    #    pci_pio_base=0x2f000000, pci_mem_base=0x40000000, int_base=100, int_count=4)

    # Uart
    uart = Uart8250(pio_addr=0x10000000)
    # Int source ID to redirect console interrupts to
    # Set to 0 if using a pci interrupt for Uart instead
    uart_int_id = Param.Int(0xa, "PLIC Uart interrupt ID")
    terminal = Terminal()

    # Dummy param for generating devicetree
    cpu_count = Param.Int(0, "dummy")

    def _on_chip_devices(self):
        """Returns a list of on-chip peripherals
        """
        return [
            self.clint,
            self.plic
        ]

    def _off_chip_devices(self):
        """Returns a list of off-chip peripherals
        """
        devices = [self.uart]
        if hasattr(self, "disk"):
            devices.append(self.disk)
        return devices

    def _on_chip_ranges(self):
        """Returns a list of on-chip peripherals
            address range
        """
        return [
            AddrRange(dev.pio_addr, size=dev.pio_size)
            for dev in self._on_chip_devices()
        ]

    def _off_chip_ranges(self):
        """Returns a list of off-chip peripherals
            address range
        """
        return [
            AddrRange(dev.pio_addr, size=dev.pio_size)
            for dev in self._off_chip_devices()
        ]

    def attachPlic(self):
        """Count number of PLIC interrupt sources
        """
        plic_srcs = [self.uart_int_id]
        #plic_srcs.append(self.pci_host.int_base)  #PCI
        for device in self._off_chip_devices():
            if hasattr(device, "interrupt_id"):
                plic_srcs.append(device.interrupt_id)
        self.plic.n_src = max(plic_srcs) + 1

    def attachOnChipIO(self, bus):
        """Attach on-chip IO devices, needs modification
            to support DMA and PCI
        """
        for device in self._on_chip_devices():
            device.pio = bus.mem_side_ports

    def attachOffChipIO(self, bus):
        """Attach off-chip IO devices, needs modification
            to support DMA and PCI
        """
        for device in self._off_chip_devices():
            device.pio = bus.mem_side_ports

    def generateDeviceTree(self, state):
        cpus_node = FdtNode("cpus")
        cpus_node.append(FdtPropertyWords("timebase-frequency", [10000000]))
        yield cpus_node

        node = FdtNode("soc")
        local_state = FdtState(addr_cells=2, size_cells=2)
        node.append(local_state.addrCellsProperty())
        node.append(local_state.sizeCellsProperty())
        node.append(FdtProperty("ranges"))
        node.appendCompatible(["simple-bus"])

        for subnode in self.recurseDeviceTree(local_state):
            node.append(subnode)

        yield node

    def annotateCpuDeviceNode(self, cpu, state):
        cpu.append(FdtPropertyStrings('mmu-type', 'riscv,sv48'))
        cpu.append(FdtPropertyStrings('status', 'okay'))
        cpu.append(FdtPropertyStrings('riscv,isa', 'rv64imafdcsu'))
        cpu.appendCompatible(["riscv"])

        int_node = FdtNode("interrupt-controller")
        int_state = FdtState(interrupt_cells=1)
        int_node.append(int_state.interruptCellsProperty())
        int_node.append(FdtProperty("interrupt-controller"))
        int_node.appendCompatible("riscv,cpu-intc")

        cpus = self.system.unproxy(self).cpu
        phandle = int_state.phandle(cpus[self.cpu_count])
        self.cpu_count += 1
        int_node.append(FdtPropertyWords("phandle", [phandle]))

        cpu.append(int_node)
