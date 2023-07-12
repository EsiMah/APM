# APM
This code is developed for demonstration purpose to calrify the method used in a scientific paper titled  "A Data-Driven Simulation-based Decision Support for Resource Allocation in Manufacturing Systems of Industry 4.0", Authored by Ehsan Mahmoodi et al. (2023).
This repository is a simplified implementation of a data-driven bottleneck detection method, namely, Active Period Method (APM), originally proposed by "Roser, Christoph, Mukund Subramaniyan, Anders Skoogh, and Björn Johansson. “An Enhanced Data-Driven Algorithm for Shifting Bottleneck Detection.” IFIP Advances in Information and Communication Technology 630 IFIP (September 5, 2021): 683–89."
# Active Period Method
The active period method is a bottleneck analysis method that works based on the state of the resources. This method can be used to find the bottlenecks that limit the throughput of a system. 
## DOI
[![DOI](https://zenodo.org/badge/664727811.svg)](https://zenodo.org/badge/latestdoi/664727811)
# Structure of the code
This version of the software gets the number of resources (R) and the number of obeservations (O), and then generates a random dataset of zeros and ones with size (R*O) to show the inactive and active periods of each resource. For instance following matix is gnereated for 3 resources and 10 observations (whihc code be 10 seconds or mintes). Zeros and ones shows the state cahnges for each resource. 
[0 0 0 1 1 0 1 0 1 0
 0 1 0 1 0 0 1 1 0 0
 0 0 0 0 1 1 0 0 1 0]
# How to use
## Option 1
  1- Download the repository
  2- install the requirements
  3- run the APM.py file
## Option 2: Download and run exe file 
The EXE version  is accessible throuhg the following link:
  https://1drv.ms/u/s!Al86AoNSSWO2g8geKCg7517jcJviDQ?e=6QwU3p
### after running the file the user needs to selct the numbner of resources and number of observations and the dataset for resources will be automatically generated.  
![Screenshot 2023-07-12 192941](https://github.com/EsiMah/APM/assets/125956561/8be4e19d-3b59-4471-89ae-3bb2cdf078c6)
