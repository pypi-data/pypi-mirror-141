#!/bin/env python3

import click
import logging
import os
import subprocess
import tempfile
import struct
import sys
import csv
import binascii
from .idrc_esp_tools import analyze_nvs


logger = logging.getLogger('configurer')
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(__file__)
TMP_DIR = os.path.join(os.environ['HOME'], '.hwtester')

NVS_TARGET_NAMESPACE = 'ESP-MDF'
exit_code = 0


class SerialDumper:

    def __init__(self, usb_port, baudrate):
        self.usb_port = usb_port
        self.baudrate = baudrate

    def get_nvs(self, nvs_key):

        partition_table_out = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR, suffix='.bin')
        nvs_partition_in = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR, suffix='.bin')
        nvs_csv_in = tempfile.NamedTemporaryFile(delete=False, dir=TMP_DIR, suffix='.csv')

        try:

            # dump partition table from a running node
            p = subprocess.run([
                'python3', '-m', 'esptool',
                '--after',
                'no_reset',
                '-p',
                self.usb_port,
                'read_flash',
                '0x8000',
                '0x1000',
                partition_table_out.name,
            ], capture_output=True, text=True)
            if p.stderr:
                logger.warning(p.stderr)
            p.check_returncode()
            logger.info('Dumped partition table')

            # read partition table to determine offset / size
            nvs_partition_offset = None
            nvs_partition_size = None
            p = subprocess.run([
                'python3',
                os.path.join(BASE_DIR, 'idrc_esp_tools/gen_esp32part.py'),
                '-q',
                partition_table_out.name,
            ], capture_output=True, text=True)
            if p.stderr:
                logger.warning(p.stderr)
            p.check_returncode()
            for line in p.stdout.split('\n'):
                if ',data,nvs,' in line:
                    _name, _type, _subtype, _offset, _size, _flags = line.strip().split(',')
                    nvs_partition_offset = int(_offset)
                    nvs_partition_size = int(_size)
                    logger.info('Detected NVS partition sized %d', nvs_partition_size)
            if nvs_partition_offset is None:
                logger.critical('Cannot find NVS partition!')
                sys.exit(1)

            # dump NVS from a running node
            p = subprocess.run([
                'python3', '-m', 'esptool',
                '--after',
                'no_reset',
                '-p',
                self.usb_port,
                'read_flash',
                str(nvs_partition_offset),
                str(nvs_partition_size),
                nvs_partition_in.name,
            ], capture_output=True, text=True)
            if p.stderr:
                logger.warning(p.stderr)
            p.check_returncode()
            logger.info('Dumped NVS partition')

            # get CSV of NVS values
            with open(nvs_partition_in.name, 'rb') as f:
                nvs_data = f.read()
                analyze_nvs.verify_nvs_size(nvs_data)
                analyze_nvs.parse_nvs_binary(nvs_data)
                for line in analyze_nvs.get_nvs_data(only_namespace=NVS_TARGET_NAMESPACE):
                    nvs_csv_in.write(line.encode() + b'\n')
                nvs_csv_in.close()
            if p.stderr:
                logger.warning(p.stderr)
            p.check_returncode()
            logger.info('Converted NVS to CSV')

            # change vals in CSV
            with open(nvs_csv_in.name) as csv_in:
                reader = csv.DictReader(csv_in)
                for row in reader:
                    if row['key'] == nvs_key:
                        return binascii.unhexlify(row['value'])

        finally:

            # cleanup
            os.unlink(nvs_csv_in.name)
            os.unlink(nvs_partition_in.name)
            os.unlink(partition_table_out.name)


@click.command()
@click.option('-p', '--port', type=str, required=True, help='USB port to open serial to.')
@click.option('-b', '--baudrate', type=int, default=115200, help='Port baudrate.')
def main(
    port,
    baudrate,
):

    runner = SerialDumper(usb_port=port, baudrate=baudrate)
    data = runner.get_nvs('mconfig_data')

    (
        router_ssid,
        router_password,
        router_bssid,
        mesh_id,
        mesh_password,
        mesh_type,
        channel,
        channel_switch_disable,
        router_switch_disable,
        mqtt_uri,
        _,
    ) = struct.unpack(
        '32s' # char router_ssid[32];
        '64s' # char router_password[64];
        '6s' # uint8_t router_bssid[6];
        '6s' # uint8_t mesh_id[6];
        '64s' # char mesh_password[64];
        'B' # mwifi_node_type_t mesh_type;
        'B' # uint8_t channel;
        'B' # uint8_t channel_switch_disable;
        'B' # uint8_t router_switch_disable;
        '128s' # uint8_t custom[32 + 96];
        'H', # uint16_t whitelist_size;
        data[:306]
    )

    mesh_type = {
        0: 'idle',
        1: 'root',
        2: 'node',
        3: 'leaf',
        4: 'sta',
    }.get(mesh_type)

    print('router_ssid =', router_ssid.rstrip(b'\x00').decode())
    print('router_password =', router_password.rstrip(b'\x00').decode())
    print('router_bssid =', binascii.hexlify(router_bssid).decode())
    print('mesh_id =', binascii.hexlify(mesh_id).decode())
    print('mesh_password =', mesh_password.rstrip(b'\x00').decode())
    print('mesh_type =', mesh_type)
    print('channel =', channel)
    print('channel_switch_disable =', channel_switch_disable)
    print('router_switch_disable =', router_switch_disable)
    print('mqtt_uri =', mqtt_uri.rstrip(b'\x00').decode())


def _main():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)-10s %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    main()


def run_dumper():
    os.makedirs(TMP_DIR, exist_ok=True)
    _main()


if __name__ == '__main__':
    run_dumper()
