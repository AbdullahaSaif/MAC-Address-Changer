import subprocess

class MacChanger:
    def __init__(self, interface):
        self.interface = interface

    def get_current_mac(self):
        try:
            result = subprocess.run(["ip", "link", "show", self.interface], capture_output=True, text=True, check=True)
            for line in result.stdout.split('\n'):
                if "link/ether" in line:
                    return line.split()[1]
            return None
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Could not retrieve MAC address: {e}")
            return None

    def change_mac(self, new_mac):
        try:
            print(f"[INFO] Changing MAC address of {self.interface} to {new_mac}")
            subprocess.run(["sudo", "ip", "link", "set", "dev", self.interface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "dev", self.interface, "address", new_mac], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "dev", self.interface, "up"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to change MAC address: {e}")

    def verify_change(self):
        current_mac = self.get_current_mac()
        if current_mac:
            print(f"[INFO] Current MAC address: {current_mac}")
        return current_mac

# Example usage:
if __name__ == "__main__":
    interface = "eth0"  # replace with your network interface
    new_mac = "00:11:22:33:44:55"  # replace with the desired new MAC address

    mac_changer = MacChanger(interface)

    current_mac = mac_changer.get_current_mac()
    if current_mac:
        print(f"Current MAC address: {current_mac}")
    
    mac_changer.change_mac(new_mac)

    if mac_changer.verify_change() == new_mac:
        print("MAC address successfully changed!")
    else:
        print("Failed to change MAC address.")
