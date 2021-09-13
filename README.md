# GNU Radio USRP AoA
GNU Radio package implementing MUSIC and root MUSIC angle of arrival algorithms with blocks necessary to provide phase synchronization of USRP devices.
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
git clone https://github.com/MarcinWachowiak/GNU-Radio-USRP-AoA
cd GNU-Radio-USRP-Beamforming/gr-aoa

mkdir build
cd build
cmake ..
make -j$(nproc)

sudo make install
sudo ldconfig
```
This repository also contains simulation of MUSIC algorithm and parametric analysis implemented in Python.

**Exemplary simulation results:**

<p align="center">
  <img src="img/aoa_sim_snr_sweep.png" width="600" alt="exemplary_simulation_img"/>
</p>

