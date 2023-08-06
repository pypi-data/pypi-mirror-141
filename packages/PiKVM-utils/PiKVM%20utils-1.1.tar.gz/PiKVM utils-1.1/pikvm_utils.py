import bz2
import csv
import getpass
import os
import re
import subprocess
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor

import paramiko
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if len(sys.argv) < 2:
    print("Example usage:\npython find_my_pi.py en0 10.0.0.1/24\npython find_my_pi.py en0")
    exit(2)

oui_file = "oui.txt"
if not os.path.exists(oui_file):
    print(f"{oui_file} not found, downloading...")
    oui_index = "https://linuxnet.ca/ieee/oui.txt.bz2"
    print(f"Downloading from: {oui_index}")
    r = requests.get(oui_index)
    b = bz2.BZ2Decompressor()
    print("Writing index to file...")
    with open(oui_file, "wb") as f:
        f.write(b.decompress(r.content))
    print("Done")

lookup_table = {}

print("Collecting OUI data...")
with open("oui.txt", "r") as f:
    for line in f.readlines():
        m = re.match(r"^([0-9A-F]{6})\s+\(base 16\)\s+(.*?)$", line)
        if m:
            mac_prefix, name = m.groups()
            lookup_table[mac_prefix] = name

if len(sys.argv) == 3:
    print("Calling nmap...")
    p = subprocess.Popen(f"nmap -sP {sys.argv[2]}".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, _ = p.communicate()
    assert p.returncode == 0

print("Calling arp-scan...")
p = subprocess.Popen(
    f"sudo arp-scan -I {sys.argv[1]} --localnet".split(" "),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    close_fds=True
)
stdout, stderr = p.communicate()
assert p.returncode == 0

print("Finding PiKVMs...")

pikvm_user = "root"
pikvm_pass = "root"


def get_ssh(ip):
    global pikvm_user, pikvm_pass

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ssh.connect(ip, username=pikvm_user, password=pikvm_pass)
    return ssh


def test_ssh(ip):
    try:
        get_ssh(ip)
        return True
    except:
        return False


def check_pikvm(arg):
    ip, mac, name = arg

    oui_name = lookup_table.get(mac.replace(":", "")[:6].upper(), None)
    if oui_name and "Raspberry" not in oui_name:
        return

    url = f"https://{ip}/"
    try:
        r = requests.get(url, verify=False, timeout=5)
    except:
        return

    if r.status_code != 200 or r.content.decode().find("<title>PiKVM Login</title>") == -1:
        return

    ssh_default = test_ssh(ip)

    print(f"PiKVM found: {url}" + (" with default SSH user/pass" if ssh_default else ""))
    return ip, ssh_default


with ThreadPoolExecutor(max_workers=8) as executor:
    found_pis = list(
        filter(
            lambda x: x is not None,
            executor.map(check_pikvm, [tuple(x.split("\t")) for x in stdout.decode().splitlines()[2:-3]])
        )
    )

if not found_pis:
    print("No PiKVMs found!")
    exit(1)

# Source: https://docs.pikvm.org/edid/#default-edid
edid_1080 = """00FFFFFFFFFFFF005262888800888888
1C150103800000780AEE91A3544C9926
0F505425400001000100010001000100
010001010101D32C80A070381A403020
350040442100001E7E1D00A050001940
3020370080001000001E000000FC0050
492D4B564D20566964656F0A000000FD
00323D0F2E0F000000000000000001C4
02030400DE0D20A03058122030203400
F0B400000018E01500A0400016303020
3400000000000018B41400A050D01120
3020350080D810000018AB22A0A05084
1A3030203600B00E1100001800000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000045"""

edid_1280 = """00FFFFFFFFFFFF005262888800888888
1C150103800000780AEE91A3544C9926
0F505425400001000100010001000100
010001010101D51B0050500019400820
B80080001000001EEC2C80A070381A40
3020350040442100001E000000FC0050
492D4B564D20566964656F0A000000FD
00323D0F2E0F0000000000000000014D
02030400DE0D20A03058122030203400
F0B400000018E01500A0400016303020
3400000000000018B41400A050D01120
3020350080D810000018AB22A0A05084
1A3030203600B00E1100001800000000
00000000000000000000000000000000
00000000000000000000000000000000
00000000000000000000000000000045"""

edid_path = "/etc/kvmd/tc358743-edid.hex"

boot_config_path = "/boot/config.txt"


def list_ips():
    for i, (ip, ssh_default) in enumerate(found_pis):
        print(f"{i+1}: {ip}" + ("" if ssh_default else " (SSH requires manual user/pass)"))


def pick_ip():
    global pikvm_user, pikvm_pass
    list_ips()
    c = input("Pick number: ")
    ip, ssh_available = found_pis[int(c) - 1]

    for _ in range(3):
        if not ssh_available:
            pikvm_user = input("SSH user to use: ")
            pikvm_pass = getpass.getpass("SSH password to use: ")

        if test_ssh(ip):
            ssh_available = True
            break
        else:
            print(f"Wrong user/password for SSH to {ip}")
    else:
        print(f"Failed to login using SSH")
        exit(1)

    return ip, ssh_available


def ssh_exec(ip, command, ignore_stderr=False):
    with get_ssh(ip) as ssh:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        stdout = ssh_stdout.read()
        stderr = ssh_stderr.read()
        assert stdout == b"", stdout
        if not ignore_stderr:
            assert stderr == b"", stderr


def edid0(ip):
    ssh_exec(ip, f"cp /usr/share/kvmd/configs.default/kvmd/tc358743-edid.hex {edid_path}")
    ssh_exec(ip, f"v4l2-ctl --device=/dev/kvmd-video --set-edid=file={edid_path} --fix-edid-checksums")
    print("EDID default restored!")


def edid1(ip):
    ssh_exec(ip, f"rw && cat << EOF > {edid_path}\n{edid_1080}\nEOF")
    ssh_exec(ip, f"v4l2-ctl --device=/dev/kvmd-video --set-edid=file={edid_path} --fix-edid-checksums")
    print("EDID 1920x1080 written!")


def edid2(ip):
    ssh_exec(ip, f"rw && cat << EOF > {edid_path}\n{edid_1280}\nEOF")
    ssh_exec(ip, f"v4l2-ctl --device=/dev/kvmd-video --set-edid=file={edid_path} --fix-edid-checksums")
    print("EDID 1280x1024 written!")


def oled(ip):
    ssh_exec(ip, "systemctl enable --now kvmd-oled kvmd-oled-reboot kvmd-oled-shutdown", ignore_stderr=True)
    ssh_exec(ip, "systemctl enable --now kvmd-fan", ignore_stderr=True)
    print("OLED enabled!")


def btwifi_off(ip):
    ssh_exec(
        ip,
        f"egrep '^dtoverlay=disable-wifi' {boot_config_path} >>/dev/null || echo 'dtoverlay=disable-wifi' >> {boot_config_path}"
    )
    ssh_exec(
        ip,
        f"egrep '^dtoverlay=disable-bt' {boot_config_path} >>/dev/null || echo 'dtoverlay=disable-bt' >> {boot_config_path}"
    )
    print("Bluetooth and WiFi disabled!")


def btwifi_on(ip):
    ssh_exec(ip, f'rw && sed -i "/^dtoverlay=disable-bt$/d" /boot/config.txt')
    ssh_exec(ip, f'rw && sed -i "/^dtoverlay=disable-wifi$/d" /boot/config.txt')
    print("Bluetooth and WiFi enabled!")


def reboot(ip):
    ssh_exec(ip, "reboot")
    print("Rebooting!")


def rootpass(ip):
    print("Changing root password")
    while True:
        new_pass = getpass.getpass("New root password: ")
        new_pass2 = getpass.getpass("Repeat new root password: ")
        if new_pass != new_pass2:
            print("Passwords didn't match!")
            continue
        break
    with get_ssh(ip) as ssh:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("passwd root")
        ssh_stdin.write(f"{new_pass}\n{new_pass}\n")
        stdout = ssh_stdout.read()
        stderr = ssh_stderr.read()
        assert stdout == b"", stdout
        assert stderr.endswith(b"password updated successfully\n"), stderr


def change_hostname(ip):
    hostname = input("New hostname: ")
    ssh_exec(ip, f"hostnamectl set-hostname {hostname}")
    print("Hostname changed!")


def change_webadmin(ip):
    print("Changing web admin password")
    while True:
        new_pass = getpass.getpass("New web admin password: ")
        new_pass2 = getpass.getpass("Repeat new web admin password: ")
        if new_pass != new_pass2:
            print("Passwords didn't match!")
            continue
        break
    with get_ssh(ip) as ssh:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("kvmd-htpasswd set admin")
        ssh_stdin.write(f"{new_pass}\n{new_pass}\n")
        stdout = ssh_stdout.read()
        stderr = ssh_stderr.read()
        assert stdout == b"", stdout
        assert stderr.endswith(b"password updated successfully\n"), stderr


def query_yes_no(question):
    while True:
        c = input(f"{question} [Y/n]")
        if c in ["", "Y", "yes", "Yes", "y"]:
            return True
        elif c in ["N", "no", "No", "n"]:
            return False
        else:
            print("Please respond with yes or no, Y or N")


def main():
    while True:
        print("Choose option:")
        print(
            """
        i: Interactive
        edid0: Restore EDID data on PiKVM to default settings
        edid1: Overwrite EDID data on PiKVM with 1920x1080 UEFI-compatible
        edid2: Overwrite EDID data on PiKVM with 1280x1024 UEFI-compatible
        oled: Enable OLED display on PiKVM v3 hat
        btwifi_off: Disable Bluetooth and WiFi
        btwifi_on: Enable Bluetooth and WiFi
        reboot: Reboot PiKVM (not desktop connected to it)
        rootpass: Change root password
        hostname: Change hostname
        webadmin: Change web admin password
        q: quit
        """
        )
        try:
            c = input()
        except KeyboardInterrupt:
            break
        if c == "q":
            break
        elif c == "edid0":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            edid0(ip)
        elif c == "edid1":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            edid1(ip)
        elif c == "edid2":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            edid2(ip)
        elif c == "oled":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            oled(ip)
        elif c == "btwifi_off":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            btwifi_off(ip)
        elif c == "btwifi_on":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            btwifi_on(ip)
        elif c == "reboot":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            reboot(ip)
        elif c == "rootpass":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            rootpass(ip)
        elif c == "hostname":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            change_hostname(ip)
        elif c == "webadmin":
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"
            change_webadmin(ip)
        elif c == "i":
            print("Interactive mode!")
            ip, ssh_available = pick_ip()
            assert ssh_available, "SSH is not available"

            if query_yes_no("Overwrite EDID data to fix UEFI/BIOS menu?"):
                edid1(ip)

            if query_yes_no("Enable OLED display for PiKVM v3 hat?"):
                oled(ip)

            if query_yes_no("Disable Bluetooth and WiFi on PiKVM?"):
                btwifi_off(ip)

            if query_yes_no("Change root password?"):
                rootpass(ip)

            if query_yes_no("Change hostname?"):
                change_hostname(ip)

            if query_yes_no("Change web admin password?"):
                change_webadmin(ip)

            if query_yes_no("Reboot PiKVM?"):
                reboot(ip)

        else:
            print(f"Unknown command: {c}")
        print("")


if __name__ == "__main__":
    main()
