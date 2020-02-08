#!/usr/bin/python3

# script to solve bandit5->bandit6 challenge on overthewire.org/wargames/bandit/bandit6

import os

home_path = "/home/bandit5/inhere"

for folder in os.listdir(home_path):
        for file in os.listdir(os.path.join(home_path, folder)):
                if (os.path.getsize(os.path.join(home_path, folder, file))) != 1033:
                        pass
                else:
                        print(os.path.join(home_path, folder, file))


