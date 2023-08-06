import ipaddress
from os import add_dll_directory
from types import prepare_class
import logging
from driver_package.parker_ipa_driver import ParkerIpaDriver
from ipaddress import IPv4Address
import argparse


def main(): 
    #enable drive : python .\src\drive_switch.py --ON
    #disable drive: python .\src\drive_switch.py --OFF
    level = logging.INFO
    fmt = '[%(levelname)s] %(asctime)s %(message)s'
    logging.basicConfig(level=level, format=fmt)
    
    parser = argparse.ArgumentParser()
    parkerdriver = ParkerIpaDriver()
    parser.add_argument('--ON', dest='feature', action='store_true')
    parser.add_argument('--OFF', dest='feature', action='store_false')
    parser.set_defaults(feature=True)
    args= parser.parse_args()
    with parkerdriver.connect_ip(IPv4Address(parkerdriver.data_dict["IPAddress"]),False):
        parkerdriver.drive_switch(args.feature)
    
if __name__ == "__main__":
    main()