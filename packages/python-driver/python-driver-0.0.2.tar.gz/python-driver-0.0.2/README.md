# About

A Python driver for the "Intelligent Parker Amplifier" or IPA servo drive/controller by Park Motion

Model: IPA04-HC
Product Page: http://www.parkermotion.com/products/Servo_Drive_Controllers__7313__30_32_80_567_29.html

## Setting up a development environment

```bash
# Create virtual enviroment
python -m venv .venv

# Activate virtual environment Unix/MacOs
source .venv/Scripts/activate
# or activate on Windows
.venv\Scripts\activate.bat

# Upgrade pip (depending on the Python version installed, a newly created virtual environment will how have a version of pip that is vastly out of date)
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

## Helpful Resources

### Parker Motion Manager (PPM)

- Location: `/product_materials/Software/Parker Motion Manager Ver 2.2.1050/pmm_installer_2_2_1050.exe`
- Allows you to interact with the rail
- Has useful help documents
  - See "Parameter Reference"
  - C:\Program Files (x86)\Parker Hannifin\Parker Motion Manager\Help Files\Reference Guides.chm
- Parker Motion Manager Guide:
  - \User Guides\ACR_Programmers_Guide.pdf

### Reference IPA Add-on Instructions

- Location: `/product_materials/Software/Add On Instructions v5/IPA_AOI_Rev5.zip/IPA_AOI_v5/EthernetIP_IPA_B.pdf`
- Location: `/product_materials/Software/Add On Instructions v5/IPA_AOI_Rev5.zip/IPA_AOI_v5/Information/IPA Ethernet IP Parameter Mapping.xlsx`
- .L5X files are presumably used with certain PLC software, but there is some useful reference material in the pdfs.

### ComACRServer6 Communications Server

- Location: `/product_materials/Software/ComACRServer6x`
- An automation server that provides communications between ACR controllers and PC software applications
- Includes samples applications in VB.NET, C#, C++ and VB6

### pycomm3 documentation

- https://docs.pycomm3.dev/en/latest/index.html
- Useful pages:
  - https://docs.pycomm3.dev/en/latest/usage/cipdriver.html
  - https://docs.pycomm3.dev/en/latest/examples/generic_messaging_examples.html#generic-messaging
  - https://docs.pycomm3.dev/en/latest/api_reference/data_types.html
