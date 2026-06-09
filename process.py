"""This module contains the actual process of the robot."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import NamedTuple

import pywintypes
from itk_dev_shared_components.sap import fmcacov, multi_session


class AftaleInput(NamedTuple):
    """A named tuple for user inputs."""
    fp_nummer: str
    aftale: str


def process():
    """The main process of the robot."""
    inputs = ask_inputs()

    if not inputs:
        messagebox.showinfo("Annulleret", "Intet input givet. Robotten stopper.")
        return

    if not inputs.aftale or not inputs.fp_nummer:
        messagebox.showerror("Mangler input", "En af inputfelterne er tomme. Robotten stopper.")
        return

    try:
        session = multi_session.get_all_sap_sessions()[0]
    except pywintypes.com_error:  # pylint: disable=no-member
        messagebox.showerror("SAP ikke fundet", "SAP blev ikke fundet åben det venligst før robotten startes. Robotten stopper.")
        return

    fmcacov.open_forretningspartner(session, fp=inputs.fp_nummer)

    table = session.findById("wnd[0]/usr/tabsDATA_DISP/tabpDATA_DISP_FC1/ssubDATA_DISP_SCA:RFMCA_COV:0202/cntlRFMCA_COV_0100_CONT5/shellcont/shell")

    # Filter on aftale
    table.setCurrentCell(-1, "VTREF")
    table.selectColumn("VTREF")
    table.contextMenu()
    table.selectContextMenuItem("&FILTER")
    session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN001-LOW").text = inputs.aftale
    session.findById("wnd[1]/tbar[0]/btn[0]").press()

    for i in range(table.RowCount-1):
        if not table.GetCellValue(i, "ZZAFTALESTATUS") or table.GetCellValue(i, "ZZSBS_EFI_AGRTYPE") != "IN":
            continue

        # Vis aftale
        table.setCurrentCell(i, "ZZAFTALESTATUS")
        table.contextMenu()
        table.selectContextMenuItem("VISAFT_EFI")

        # Luk aftale
        session.findById("wnd[0]/tbar[1]/btn[25]").press()
        session.findById("wnd[0]/tbar[1]/btn[24]").press()
        session.findById("wnd[1]/usr/btnBUTTON_1").press()
        session.findById("wnd[0]/tbar[0]/btn[3]").press()

    messagebox.showinfo("Færdig", f"Alle IN aftaler på fp {inputs.fp_nummer} aftale {inputs.aftale} er blevet lukket.")


def ask_inputs() -> AftaleInput | None:
    """Ask the user for an fp and aftale number.

    Returns:
        A named tuple with the inputs or none if canceled.
    """
    result: dict[str, str] = {}

    root = tk.Tk()
    root.title("Lukning af aftaler")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=12)
    frame.grid()

    ttk.Label(frame, text="FP-nummer:").grid(row=0, column=0, sticky="w", pady=4)
    fp_entry = ttk.Entry(frame, width=30)
    fp_entry.grid(row=0, column=1, pady=4)

    ttk.Label(frame, text="Aftale:").grid(row=1, column=0, sticky="w", pady=4)
    aftale_entry = ttk.Entry(frame, width=30)
    aftale_entry.grid(row=1, column=1, pady=4)

    def on_ok():
        result["fp_nummer"] = fp_entry.get()
        result["aftale"] = aftale_entry.get()
        root.destroy()

    def on_cancel():
        root.destroy()

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=2, column=0, columnspan=2, pady=(8, 0), sticky="e")
    ttk.Button(button_frame, text="Cancel", command=on_cancel).grid(row=0, column=0, padx=4)
    ttk.Button(button_frame, text="OK", command=on_ok).grid(row=0, column=1)

    root.bind("<Return>", lambda _: on_ok())
    root.bind("<Escape>", lambda _: on_cancel())
    fp_entry.focus_set()

    root.mainloop()

    if not result:
        return None

    return AftaleInput(fp_nummer=result["fp_nummer"], aftale=result["aftale"])


if __name__ == "__main__":
    process()
