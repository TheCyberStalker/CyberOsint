import requests
import os
import json
from colorama import init, Fore, Style
import socket
from faker import Faker
import time
import sys
from pathlib import Path
import telebot
from telebot import types

init(autoreset=True)

# Определяем путь к директории, где находится скрипт
SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "cyberosint_config.json"

API_URL = "https://server.leakosint.com/"
fake = Faker()

BANNER = f"""
{Fore.GREEN}{Style.BRIGHT.center(80)}
   ██████╗██╗   ██╗██████╗ ███████╗██████╗    
  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗   
  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝     
  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗      
  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║    
   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝     
                 ██████╗ ███████╗██╗███╗   ██╗████████╗
                ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
                ██║   ██║███████╗██║██╔██╗ ██║   ██║   
                ██║   ██║╚════██║██║██║╚██╗██║   ██║   
                ╚██████╔╝███████║██║██║ ╚████║   ██║   
                 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   

                       {Fore.BLUE}::Telegram - {Fore.RED}@Y0urAdm1n::                                      
"""

MENU = f"""
{Fore.GREEN}{Style.BRIGHT.center(80)}
{Fore.GREEN}               ╔═════════════════════════════════════╗
{Fore.GREEN}               ║ {Fore.YELLOW}1. {Fore.GREEN}Поиск утечек по email            {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}2. {Fore.GREEN}Поиск утечек по юзернейму        {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}3. {Fore.GREEN}Поиск утечек по телефону         {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}4. {Fore.GREEN}Поиск по IP                      {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}5. {Fore.GREEN}Генерация случайных данных       {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}6. {Fore.GREEN}Поиск по домену                  {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}7. {Fore.GREEN}Сканер портов                    {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}8. {Fore.GREEN}Поиск по MAC-адресу              {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}9. {Fore.GREEN}Атака на номер телефона          {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}10. {Fore.GREEN}TgPhisher (ГлазБога)            {Fore.GREEN}║
{Fore.GREEN}               ║ {Fore.YELLOW}11. {Fore.GREEN}Поиск по любым данным           {Fore.GREEN}║
{Fore.GREEN}               ╚═════════════════════════════════════╝
                   
                                   {Fore.YELLOW}12. {Fore.RED}Выход       {Fore.GREEN}
                                   {Fore.YELLOW}13. {Fore.RED}Выход с удалением конфигурации  {Fore.GREEN}
                      
"""

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)

def search_leaks(request, token, limit=1000):
    data = {
        "token": token,
        "request": request,
        "limit": limit
    }
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        return handle_response(response)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")
        return {"error": "Запрос не удался"}

def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

def print_leak_info(leak_info):
    if 'NumOfResults' in leak_info and leak_info['NumOfResults'] > 0:
        for source, details in leak_info['List'].items():
            print(f"{Fore.CYAN}Источник: {Fore.GREEN}{source}")
            for record in details['Data']:
                if isinstance(record, dict):
                    for key, value in record.items():
                        if key != 'InfoLeak':
                            print(f"{Fore.CYAN}  - {key}: {Fore.GREEN}{value}")
    else:
        print(f"{Fore.RED}Результаты не найдены.")

def search_by_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()
        for key, value in data.items():
            print(f"{Fore.CYAN}{key.capitalize()}: {Fore.GREEN}{value}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка: {e}")

def logout():
    print(f"{Fore.RED}Выход...")
    exit()

def logout_and_delete_config():
    try:
        CONFIG_FILE.unlink()
        print(f"{Fore.RED}Файл конфигурации удален. Выход...")
    except FileNotFoundError:
        print(f"{Fore.RED}Файл конфигурации не найден. Выход...")
    except Exception as e:
        print(f"{Fore.RED}Произошла ошибка при удалении файла конфигурации: {e}")
    exit()

def generate_random_data():
    print(f"{Fore.CYAN}Имя: {Fore.GREEN}{fake.name()}")
    print(f"{Fore.CYAN}Адрес: {Fore.GREEN}{fake.address()}")
    print(f"{Fore.CYAN}Email: {Fore.GREEN}{fake.email()}")
    print(f"{Fore.CYAN}Телефон: {Fore.GREEN}{fake.phone_number()}")
    print(f"{Fore.CYAN}Кредитная карта: {Fore.GREEN}{fake.credit_card_full()}")
    print(f"{Fore.CYAN}Пароль: {Fore.GREEN}{fake.password()}")

def main():
    clear_screen()
    config = load_config()

    if 'name' in config and 'token' in config:
        name = config['name']
        token = config['token']
        print(f"\n     С возвращением, {name}!")
    else:
        name = input(f"Введите ваше имя: ")
        token = input(f"Введите ваш токен: ")
        config['name'] = name
        config['token'] = token
        save_config(config)
        clear_screen()
    
    while True:
        clear_screen()
        print(BANNER)
        print(MENU)
        choice = input(f"{Fore.CYAN}Введите ваш выбор: {Fore.GREEN}")
        clear_screen()
        print(BANNER)
        if choice.isdigit() and 1 <= int(choice) <= 13:
            choice = int(choice)
            if choice == 1:
                email = input(f"{Fore.CYAN}Введите email: {Fore.GREEN}")
                limit = input(f"{Fore.CYAN}Введите лимит (100-10000, по умолчанию 1000(enter)): {Fore.GREEN}") or 1000
                limit = int(limit)
                result = search_leaks(email, token, limit)
                print_leak_info(result)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 2:
                username = input(f"{Fore.CYAN}Введите имя пользователя: {Fore.GREEN}")
                limit = input(f"{Fore.CYAN}Введите лимит (100-10000, по умолчанию 1000(enter)): {Fore.GREEN}") or 1000
                limit = int(limit)
                result = search_leaks(username, token, limit)
                print_leak_info(result)
                input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")
            elif choice == 12:
                logout()
            elif choice == 13:
                logout_and_delete_config()
        else:
            print(f"{Fore.RED}Неверный выбор, попробуйте снова.")
            input(f"\n{Fore.CYAN}Нажмите Enter для возврата в меню >> ")

if __name__ == "__main__":
    main()
