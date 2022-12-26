#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://192.168.1.1', help="router's control addr")
parser.add_argument('password', help="router's control password")
parser.add_argument('hostname', help="domain to update")
parser.add_argument('ddns-password', help="ddns password")


def get_wanip(url: str, password):
    """Get WAN IP

    For Huawei AX3
    """
    options = Options()
    options.headless = True
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)

        try:
            elem = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, 'userpassword_ctrl'))
            )
        except Exception as e:
            raise e(f"Timeout opening router's control page {url}")

        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.ENTER)

        try:
            elem = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.wanip > .content'))
            )
        except Exception as e:
            raise e(f"Timeout logging in router")

        return elem.text


def update_ddns(ip, hostname, password):
    """Update DDNS

    For he.net
    """
    print(f'updating ddns: {hostname} -> {ip}')
    r = requests.get(
        f'https://dyn.dns.he.net/nic/update?hostname={hostname}&'
        f'password={password}&myip={ip}'
    )
    print(f'response: {r.text}')


def main():
    args = parser.parse_args()
    ip = get_wanip(args.url, args.password)
    update_ddns(ip, args.hostname, vars(args)['ddns-password'])


if __name__ == '__main__':
    main()
