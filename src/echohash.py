# This file is part of EchoHash.
# Copyright (C) 2025 elbenis
#
# EchoHash is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#  ______     _           _    _           _     
# |  ____|   | |         | |  | |         | |    
# | |__   ___| |__   ___ | |__| | __ _ ___| |__  
# |  __| / __| '_ \ / _ \|  __  |/ _` / __| '_ \ 
# | |___| (__| | | | (_) | |  | | (_| \__ \ | | |
# |______\___|_| |_|\___/|_|  |_|\__,_|___/_| |_|
#

import secrets
import sympy
import math
import time
import getpass
import random
from colorama import Fore, Back, Style

# EchoHash
def EchoHash(secret):
    hash = ""

    for i in range(len(secret)):
        char = secret[i]
        w = len(secret)
        x = ((w * 0x5bd1e995) ^ (w << 13)) + 0x7fffffff

        if char.isdigit():
            charResult = math.exp(math.sin(int(char)) + math.log(abs(int(char)) + 1)) + int(char)**len(secret)
            charResult = charResult + math.log((pow(x, 65537, 10**9 + 7) % (10**8)) + 1)
            charResult = charResult + math.log((pow(x, 2**16 + 1, 10**9 + 9) % 10**8) + 1)
            charResult = charResult + math.log(abs(pow(x, 3, 10**9 + 7)) + 1)
            charResult = charResult + math.log1p(pow(x, 17, 10**9 + 7) % 10**6)

        elif char.isalpha():
            char_num = ord(char)
            fraction = (char_num / 256)
            charResult = math.sin(fraction * 3.99 * (1 - fraction))
            charResult = charResult + math.sin(x**3) + math.log(x + 2) + math.sqrt(x**2 + 1)
            charResult = charResult + math.sin((x % 1) * 3.99 * (1 - (x % 1)))
            charResult = charResult + math.cos(pow(x, 65537, 10**9 + 7) % 360)
            charResult = charResult + math.sin(x**5) + math.log(abs(x) + 3) + math.sqrt(x**2 + 7)
            charResult = charResult + math.exp(-((x % 1000) / 500)) * math.sin(x**2 + 1)
            charResult = charResult + math.exp(math.cos(x % 10) * math.log(x + 2))
            charResult = charResult + math.sin(pow(x, 12345, 10**9 + 7) % 360)
            charResult = charResult + math.exp(-abs(x % 50) / 25) * math.cos(x**2 + 1)

        # Final operations
        charResult = str(charResult)
        charResult = charResult.replace(".", "")

        try:
            charResult = abs(int(float(charResult)))
        except ValueError:
            charResult = abs(ord(charResult)) if isinstance(charResult, str) else abs(charResult)

        accumulated = sum(ord(c) for c in hash) & 0xFFFFFFFF
        charResult = (charResult ^ ((accumulated << 3) | (accumulated >> 29))) & 0xFFFFFFFF

        if i != 0:
            prev_char = ord(hash[-1])

            prev_char = (prev_char << 3) ^ 0b10101
            prev_char = (prev_char | 0b111000) & 0b101111
            prev_char = (prev_char + 0b1001) * 0b110
            prev_char = prev_char ^ (prev_char >> 4)
            prev_char = prev_char & 0xFFFFFFFF

            charResult = sum(ord(c) for c in str(charResult)) + ord("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"[((((prev_char if isinstance(prev_char,int) else ord(prev_char)) << 5) | ((charResult if isinstance(charResult,int) else ord(charResult)) >> 3)) ^ ((charResult if isinstance(charResult,int) else ord(charResult)) * 7) + ((prev_char if isinstance(prev_char,int) else ord(prev_char)) ^ (charResult if isinstance(charResult,int) else ord(charResult)))) % 62])

        hash = hash + str(charResult)

    # Make it 128 characters
    base62chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    seed = 0
    for i, c in enumerate(hash):
        seed ^= (ord(c) << (i % 64))
        seed = (seed * 0x5bd1e995) & 0xFFFFFFFFFFFFFFFF


    rng = random.Random(seed)

    final_hash = "".join(rng.choice(base62chars) for _ in range(128))

    return final_hash


# Manager
def manager():
    global inp

    print("Hash a password with EchoHash: 1")
    print("Hash testing: 2")

    try:
        inp = int(input("> "))
    except:
        print(Fore.RED + "Choose a valid option.\n" + Style.RESET_ALL)
        time.sleep(1)
        manager()
    
    # Hash
    if inp == 1:
        secretINP = getpass.getpass("Secret: ")
        secretINPcheck = getpass.getpass("Confirm Secret: ")

        if secretINP == secretINPcheck:
            print(EchoHash(secretINP))
        else:
            print(Fore.RED + "Secrets are not equal.\n" + Style.RESET_ALL)
            time.sleep(1)
            manager()
    
    # Hash Testing (I use this for testing the hash method).
    if inp == 2:
        passwords = ["password123", "password122", "password121", "passwo123", "passwords123"]

        for i in range(len(passwords)):
            print(EchoHash(passwords[i]))

manager()