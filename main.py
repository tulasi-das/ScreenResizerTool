import ctypes
import tkinter as tk
from tkinter import messagebox


class DISPLAY_DEVICEW(ctypes.Structure):
    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("DeviceName", ctypes.c_wchar * 32),
        ("DeviceString", ctypes.c_wchar * 128),
        ("StateFlags", ctypes.c_ulong),
        ("DeviceID", ctypes.c_wchar * 128),
        ("DeviceKey", ctypes.c_wchar * 128),
    ]


class DEVMODEW(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", ctypes.c_ushort),
        ("dmDriverVersion", ctypes.c_ushort),
        ("dmSize", ctypes.c_ushort),
        ("dmDriverExtra", ctypes.c_ushort),
        ("dmFields", ctypes.c_ulong),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", ctypes.c_ushort),
        ("dmBitsPerPel", ctypes.c_ulong),
        ("dmPelsWidth", ctypes.c_ulong),
        ("dmPelsHeight", ctypes.c_ulong),
        ("dmDisplayFlags", ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
        ("dmICMMethod", ctypes.c_ulong),
        ("dmICMIntent", ctypes.c_ulong),
        ("dmMediaType", ctypes.c_ulong),
        ("dmDitherType", ctypes.c_ulong),
        ("dmReserved1", ctypes.c_ulong),
        ("dmReserved2", ctypes.c_ulong),
        ("dmPanningWidth", ctypes.c_ulong),
        ("dmPanningHeight", ctypes.c_ulong),
    ]


user32 = ctypes.WinDLL('user32', use_last_error=True)

ENUM_CURRENT_SETTINGS = -1
CDS_UPDATEREGISTRY = 0x00000001
CDS_TEST = 0x00000002
DISP_CHANGE_SUCCESSFUL = 0


def enum_display_devices():
    devices = []
    i = 0
    while True:
        dd = DISPLAY_DEVICEW()
        dd.cb = ctypes.sizeof(dd)
        res = user32.EnumDisplayDevicesW(None, i, ctypes.byref(dd), 0)
        if not res:
            break
        devices.append({'name': dd.DeviceName, 'string': dd.DeviceString})
        i += 1
    return devices


def enum_modes(device_name):
    modes = []
    i = 0
    dm = DEVMODEW()
    dm.dmSize = ctypes.sizeof(dm)
    while True:
        res = user32.EnumDisplaySettingsW(device_name, i, ctypes.byref(dm))
        if not res:
            break
        modes.append({
            'width': dm.dmPelsWidth,
            'height': dm.dmPelsHeight,
            'bits': dm.dmBitsPerPel,
            'freq': dm.dmDisplayFrequency,
        })
        i += 1
    return modes


def apply_mode(device_name, width, height, bits=None, freq=None):
    dm = DEVMODEW()
    dm.dmSize = ctypes.sizeof(dm)
    dm.dmPelsWidth = int(width)
    dm.dmPelsHeight = int(height)
    flags = 0
    DM_PELSWIDTH = 0x80000
    DM_PELSHEIGHT = 0x100000
    DM_BITSPERPEL = 0x40000
    DM_DISPLAYFREQUENCY = 0x400000
    dm.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT
    if bits:
        dm.dmBitsPerPel = int(bits)
        dm.dmFields |= DM_BITSPERPEL
    if freq:
        dm.dmDisplayFrequency = int(freq)
        dm.dmFields |= DM_DISPLAYFREQUENCY

    res = user32.ChangeDisplaySettingsExW(device_name, ctypes.byref(dm), None, 0, None)
    return res


class App:
    def __init__(self, root):
        self.root = root
        root.title('Screen Resizer')

        self.devices = enum_display_devices()

        self.dev_listbox = tk.Listbox(root, height=6, exportselection=False)
        for d in self.devices:
            self.dev_listbox.insert(tk.END, f"{d['name']} - {d['string']}")
        self.dev_listbox.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')
        self.dev_listbox.bind('<<ListboxSelect>>', self.on_select_device)

        self.modes_listbox = tk.Listbox(root, height=10, exportselection=False)
        self.modes_listbox.grid(row=0, column=1, padx=8, pady=8, sticky='nsew')

        self.apply_btn = tk.Button(root, text='Apply', command=self.on_apply)
        self.apply_btn.grid(row=1, column=1, sticky='e', padx=8, pady=(0,8))

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        if self.devices:
            self.dev_listbox.selection_set(0)
            self.on_select_device()

    def on_select_device(self, event=None):
        sel = self.dev_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        device = self.devices[idx]
        self.current_device_name = device['name']
        modes = enum_modes(device['name'])
        self.modes = modes
        self.modes_listbox.delete(0, tk.END)
        seen = set()
        for m in modes:
            key = (m['width'], m['height'], m.get('bits'), m.get('freq'))
            if key in seen:
                continue
            seen.add(key)
            self.modes_listbox.insert(tk.END, f"{m['width']}x{m['height']} @ {m.get('freq',0)}Hz, {m.get('bits',0)}bpp")

    def on_apply(self):
        sel = self.modes_listbox.curselection()
        if not sel:
            messagebox.showwarning('No selection', 'Please select a mode')
            return
        idx = sel[0]
        mode = self.modes[idx]
        answer = messagebox.askyesno('Confirm', f"Change {self.current_device_name} to {mode['width']}x{mode['height']}?")
        if not answer:
            return
        res = apply_mode(self.current_device_name, mode['width'], mode['height'], mode.get('bits'), mode.get('freq'))
        if res == DISP_CHANGE_SUCCESSFUL:
            messagebox.showinfo('Success', 'Resolution changed successfully')
        else:
            messagebox.showerror('Error', f'Change failed (code {res})')


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
