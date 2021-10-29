# keysight_network_analyser_control
Scripts to control and extract data from a Keysight Network Analyser

Currently only supports Windows

## Python dependencies

External packages used at time of documentation, newer version will mostly not break scripts.

```
matplotlib==3.3.4
numpy==1.19.2
PyVISA==1.11.3
scikit_rf==0.18.1
```

## Install Keysight libraries 

Can be downloaded and installed from [here](https://www.keysight.com/us/en/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html) 

In the scripts edit  path to the appropraite library file

```
VISA_LIB_FILE_PATH = "C:\\Windows\\System32\\visa64.dll"
```
## Current scripts 

- `measure_s11.py`
- `measure_two_port_s_parameters.py`
- 
## Usage

Edit the parent directory where files and plots will be stored:
```
PARENT_DIR = "C:\\Users\\username\\Desktop\\workingdirectory\\"
```
Run script:
```
python ./measure_two_port_s_parameters
```

### TODO 
- linux support
