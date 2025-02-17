#!/usr/bin/env python3

import socket
import tkinter as tk
from tkinter import ttk
import threading
import json
import os
import subprocess

from scapy.all import ARP, Ether, srp
from scapy.config import conf
import random
import re
from Visuals import AnimationHandler
import tkinter as tk
from tkinter import ttk, messagebox
conf.L3socket

# Persistent storage file for saved devices
SAVED_DEVICES_FILE = "saved_devices.json"
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

if not is_admin():
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


def load_saved_devices():
    if os.path.exists(SAVED_DEVICES_FILE):
        with open(SAVED_DEVICES_FILE, "r") as f:
            return json.load(f)
    return []

def save_device_to_file(device):
    devices = load_saved_devices()
    # Update if device with same IP already saved
    for idx, dev in enumerate(devices):
        if dev["ip"] == device["ip"]:
            break
    else:
        devices.append(device)
    with open(SAVED_DEVICES_FILE, "w") as f:
        json.dump(devices, f)

def get_device_name(ip_addr):
    try:
        return socket.gethostbyaddr(ip_addr)[0]
    except socket.herror:
        return "Unknown"

def scan_network(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=False)[0]
    devices = []
    for sent, received in result:
        devices.append({
            "ip": received.psrc,
            "mac": received.hwsrc,
            "name": get_device_name(received.psrc)
        })
    return devices

def get_network_adapters():
    try:
        output = subprocess.check_output(
            'powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq \'Up\' } | Select-Object -ExpandProperty Name"',
            shell=True, universal_newlines=True
        )
        adapters = [line.strip() for line in output.splitlines() if line.strip()]
        return adapters
    except subprocess.CalledProcessError:
        return []

def show_gui():
    window = tk.Tk()
    window.title("Network Scanner")
    window.geometry("800x600")
    window.configure(bg="#23272a")
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("TFrame", background="#23272a")
    style.configure("TLabel", background="#23272a", foreground="#FFFFFF", font=("Helvetica", 12))
    style.configure("TButton", background="#4CAF50", foreground="#FFFFFF", font=("Helvetica", 12))
    style.configure("Treeview", background="#2c2f33", foreground="#FFFFFF", fieldbackground="#2c2f33", borderwidth=0)
    style.configure("Treeview.Heading", background="#34373c", foreground="#FFFFFF", font=("Helvetica", 12, 'bold'))
    style.map("Treeview.Heading", background=[('active', '#4a4d52')])
    
    frame = ttk.Frame(window, padding=10, style="TFrame")
    frame.pack(fill=tk.BOTH, expand=True)
    
    ip_range = "192.168.1.0/24"
    title_label = ttk.Label(frame, text="Network Scanner", font=("Helvetica", 16, "bold"), style="TLabel")
    title_label.pack(pady=(0, 20))
    
    adapters = get_network_adapters()
    adapter_label = ttk.Label(frame, text="Select Network Adapter:", style="TLabel")
    adapter_label.pack(pady=(10, 0))
    adapter_combobox = ttk.Combobox(frame, values=adapters, state="readonly", font=("Helvetica", 12))
    if adapters:
        adapter_combobox.current(0)
    adapter_combobox.pack(pady=(0, 10))
    
    scan_button = ttk.Button(frame, text="Start Scan", style="TButton")
    scan_button.pack(pady=(0, 20))
    
    progress_anim = AnimationHandler(frame)
    
    tree = ttk.Treeview(frame, columns=("IP", "MAC", "Name"), show="headings", style="Treeview")
    tree.heading("IP", text="IP Address", anchor=tk.CENTER)
    tree.heading("MAC", text="MAC Address", anchor=tk.CENTER)
    tree.heading("Name", text="Device Name", anchor=tk.CENTER)
    tree.column("IP", width=200, anchor=tk.CENTER)
    tree.column("MAC", width=250, anchor=tk.CENTER)
    tree.column("Name", width=300, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def update_row_colors():
        for item in tree.get_children():
            if tree.index(item) % 2 == 0:
                tree.item(item, tags=('even',))
            else:
                tree.item(item, tags=('odd',))
    tree.tag_configure('even', background="#23272a", foreground="#FFFFFF")
    tree.tag_configure('odd', background="#2c2f33", foreground="#FFFFFF")
    
    def start_scan():
        scan_button.config(state=tk.DISABLED)
        progress_anim.start(fill=tk.X, padx=10, pady=(0, 5))
        def thread_scan():
            scanned = scan_network(ip_range)
            window.after(0, lambda: update_tree(scanned))
        threading.Thread(target=thread_scan, daemon=True).start()
    
    def update_tree(scanned_devices):
        progress_anim.stop()
        saved_devices = load_saved_devices()
        saved_dict = {dev["ip"]: dev for dev in saved_devices}
        merged_devices = []
        scanned_ips = set()
        for dev in scanned_devices:
            scanned_ips.add(dev["ip"])
            merged_devices.append(saved_dict.get(dev["ip"], dev))
        for ip, dev in saved_dict.items():
            if ip not in scanned_ips:
                merged_devices.append(dev)
        for row in tree.get_children():
            tree.delete(row)
        for dev in merged_devices:
            tree.insert("", tk.END, values=(dev["ip"], dev["mac"], dev["name"]))
        update_row_colors()
        scan_button.config(state=tk.NORMAL)
    
    scan_button.config(command=start_scan)
    
    def randomize_mac_address():
        adapter = adapter_combobox.get()
        if not adapter:
            messagebox.showerror("Error", "Please select an adapter first.")
            return
        new_mac = generate_random_mac()
        try:
            cmd = (
                f'powershell -ExecutionPolicy Bypass -Command "'
                f'Set-NetAdapter -Name \'{adapter}\' -MacAddress \'{new_mac}\' -Confirm:$false ; '
                f'Disable-NetAdapter -Name \'{adapter}\' -Confirm:$false ; '
                f'Enable-NetAdapter -Name \'{adapter}\' -Confirm:$false"'
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Random MAC: {new_mac} was set for adapter {adapter}.")
            else:
                messagebox.showerror("Error", f"Failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def set_manual_mac_address():
        adapter = adapter_combobox.get()
        if not adapter:
            messagebox.showerror("Error", "Please select an adapter first.")
            return
        def confirm_mac():
            typed_mac = mac_entry.get().strip()
            if not re.match(r"^[0-9A-Fa-f:]{17}$", typed_mac):
                messagebox.showerror("Error", "Invalid MAC format. Example: 02:1A:2B:3C:4D:5E")
                return
            try:
                cmd = (
                    f'powershell -ExecutionPolicy Bypass -Command "'
                    f'Set-NetAdapter -Name \'{adapter}\' -MacAddress \'{typed_mac}\' -Confirm:$false ; '
                    f'Disable-NetAdapter -Name \'{adapter}\' -Confirm:$false ; '
                    f'Enable-NetAdapter -Name \'{adapter}\' -Confirm:$false"'
                )
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"MAC {typed_mac} set for adapter {adapter}.")
                else:
                    messagebox.showerror("Error", f"Failed.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            mac_window.destroy()
    
        mac_window = tk.Toplevel(window)
        mac_window.title("Set MAC Manually")
        tk.Label(mac_window, text="Enter MAC address (e.g., 02:1A:2B:3C:4D:5E):").pack(pady=5)
        mac_entry = tk.Entry(mac_window, width=20)
        mac_entry.pack(pady=5)
        tk.Button(mac_window, text="Set MAC", command=confirm_mac).pack(pady=5)
    
    def set_mac_address_to_device():
        selected = tree.focus()
        if selected:
            adapter = adapter_combobox.get()
            if not adapter:
                messagebox.showerror("Error", "Please select a network adapter.")
                return
            mac = tree.item(selected)["values"][1]
            try:
                cmd = (
                    f'powershell -ExecutionPolicy Bypass -Command "'
                    f'Set-NetAdapter -Name \'{adapter}\' -MacAddress \'{mac}\' -Confirm:$false ; '
                    f'Disable-NetAdapter -Name \'{adapter}\' -Confirm:$false ; '
                    f'Enable-NetAdapter -Name \'{adapter}\' -Confirm:$false"'
                )
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    messagebox.showinfo("Success", f"MAC Address set to {mac} for adapter {adapter}.")
                else:
                    error_msg = f"Failed to set MAC address.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
                    messagebox.showerror("Error", error_msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def copy_mac_address():
        selected = tree.focus()
        if selected:
            mac = tree.item(selected)["values"][1].replace(":", "")
            window.clipboard_clear()
            window.clipboard_append(mac)
    
    def save_selected_device():
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            device = {"ip": values[0], "mac": values[1], "name": values[2]}
            save_device_to_file(device)
    
    def on_right_click(event):
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)
            menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", on_right_click)
    
    menu = tk.Menu(window, tearoff=0)
    menu.add_command(label="Save Device", command=save_selected_device)
    menu.add_command(label="Copy MAC Address", command=copy_mac_address)
    menu.add_command(label="Set MAC Address To This Device", command=set_mac_address_to_device)
    menu.add_command(label="Randomize MAC Address", command=randomize_mac_address)
    menu.add_command(label="Set MAC Address Manually", command=set_manual_mac_address)
    
    def on_double_click(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            col = tree.identify_column(event.x)
            if col == "#3":
                iid = tree.identify_row(event.y)
                if not iid:
                    return
                values = tree.item(iid)["values"]
                x, y, width, height = tree.bbox(iid, column=col)
                entry = tk.Entry(tree)
                entry.place(x=x, y=y, width=width, height=height)
                entry.insert(0, values[2])
                entry.focus()
                def save_edit(event):
                    new_name = entry.get()
                    tree.set(iid, column="Name", value=new_name)
                    device = {"ip": values[0], "mac": values[1], "name": new_name}
                    save_device_to_file(device)
                    entry.destroy()
                entry.bind("<Return>", save_edit)
                entry.bind("<FocusOut>", lambda e: entry.destroy())
    
    tree.bind("<Double-1>", on_double_click)
    
    # Load initial devices if any
    def load_initial_devices():
        saved_devices = load_saved_devices()
        for dev in saved_devices:
            tree.insert("", tk.END, values=(dev["ip"], dev["mac"], dev["name"]))
        update_row_colors()
    load_initial_devices()
    
    window.mainloop()

def generate_random_mac():
    # Locally administered address
    mac_bytes = [0x02, random.randint(0x00, 0x7f),
                 random.randint(0x00, 0xff),
                 random.randint(0x00, 0xff),
                 random.randint(0x00, 0xff),
                 random.randint(0x00, 0xff)]
    return ':'.join(f'{b:02X}' for b in mac_bytes)

if __name__ == "__main__":
    show_gui()
