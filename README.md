# GNU Radio Angle of arrival estimation with USRP

GNU Radio package implementing MUSIC and root MUSIC angle of arrival algorithms with blocks necessary to provide phase synchronization of USRP devices. Implemented blocks include:

1. MUSIC Linear Array
2. Root-MUSIC
3. Calculate Phase Difference
4. Shift Phase
5. Correlate
6. Precise Moving Average
7. Head with Reset


This is an updated and improved version of https://github.com/EttusResearch/gr-doa.

**Implemented blocks:**
<p align="center">
  <img src="img/blocks.png" width="600" alt="implemented_blocks_img"/>
</p>

**Exemplary GR GUI:**
<p align="center">
  <img src="img/gr_inter_aoa.png" width="600" alt="exemplary_gr_gui_img"/>
</p>

**Installation procedure:**
```
cd
git git@github.com:MarcinWachowiak/gr-aoa.git
cd gr-aoa

mkdir build
cd build
cmake ..
make -j$(nproc)

sudo make install
sudo ldconfig
```

**Usage:**

For exemplary flowcharts and use cases visit examples directory
