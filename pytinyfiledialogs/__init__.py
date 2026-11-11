import ctypes
import sys
from pathlib import Path
from typing import Optional

# 1. Dynamically locate the compiled binary based on the OS
base_dir = Path(__file__).parent
if sys.platform == "win32":
    lib_path = base_dir / "libtinyfiledialogs.dll"
elif sys.platform == "darwin":
    lib_path = base_dir / "libtinyfiledialogs.dylib"
else:
    lib_path = base_dir / "libtinyfiledialogs.so"

# 2. Load the library
tfd = ctypes.CDLL(str(lib_path))

# 3. Define C function signatures
tfd.tinyfd_notifyPopup.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]
tfd.tinyfd_notifyPopup.restype = ctypes.c_int

# int tinyfd_messageBox(char* title, char* message, char* dialogType, char* iconType, int defaultButton)
tfd.tinyfd_messageBox.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int
]
tfd.tinyfd_messageBox.restype = ctypes.c_int

# char* tinyfd_inputBox(char* title, char* message, char* defaultInput)
tfd.tinyfd_inputBox.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]
tfd.tinyfd_inputBox.restype = ctypes.c_char_p

# char* tinyfd_saveFileDialog(char* title, char* defaultPath, int numFilters, char** filters, char* filterDesc)
tfd.tinyfd_saveFileDialog.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_char_p
]
tfd.tinyfd_saveFileDialog.restype = ctypes.c_char_p

# char* tinyfd_openFileDialog(char* title, char* defaultPath, int numFilters, char** filters, char* filterDesc, int allowMultiple)
tfd.tinyfd_openFileDialog.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int,
    ctypes.POINTER(ctypes.c_char_p), ctypes.c_char_p, ctypes.c_int
]
tfd.tinyfd_openFileDialog.restype = ctypes.c_char_p

# char* tinyfd_selectFolderDialog(char* title, char* defaultPath)
tfd.tinyfd_selectFolderDialog.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p
]
tfd.tinyfd_selectFolderDialog.restype = ctypes.c_char_p

# char* tinyfd_colorChooser(char* title, char* defaultHexRGB, unsigned char defaultRGB[3], unsigned char resultRGB[3])
tfd.tinyfd_colorChooser.argtypes = [
    ctypes.c_char_p, ctypes.c_char_p,
    ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)
]
tfd.tinyfd_colorChooser.restype = ctypes.c_char_p

# void tinyfd_beep(void)
tfd.tinyfd_beep.argtypes = []
tfd.tinyfd_beep.restype = None


# Helper to encode Python strings to C strings (UTF-8)
def _c_str(text):
    return text.encode('utf-8') if text is not None else None


def _decode(result):
    return result.decode('utf-8') if result else None


def _filter_args(filters, description):
    """Convert a Python filter list into C count, array, and description."""
    patterns = [str(f) for f in (filters or [])]
    if not patterns:
        return 0, None, None

    c_filters = (ctypes.c_char_p * len(patterns))(*[_c_str(f) for f in patterns])
    if description is None:
        description = f"{', '.join(patterns)} files"
    return len(patterns), c_filters, _c_str(description)


# --- PUBLIC PYTHON API ---

def notify_popup(title: str, message: str, icon_type: str = "info") -> int:
    """Shows a notification popup. Returns 1 on success."""
    return tfd.tinyfd_notifyPopup(
        _c_str(title), _c_str(message), _c_str(icon_type)
    )


def message_box(title: str, message: str, dialog_type: str = "ok", icon_type: str = "info") -> int:
    """Shows a native message box. Returns 1 for OK/Yes, 0 for Cancel/No."""
    return tfd.tinyfd_messageBox(
        _c_str(title), _c_str(message), _c_str(dialog_type), _c_str(icon_type), 1
    )


def input_box(
    title: str = "Input",
    message: str = "",
    default_input: Optional[str] = "",
) -> Optional[str]:
    """Shows an input box. Pass default_input=None for a password box."""
    result = tfd.tinyfd_inputBox(
        _c_str(title), _c_str(message), _c_str(default_input)
    )
    return _decode(result)


def save_file_dialog(
    title: str = "Save file",
    default_path: str = "",
    filters: Optional[list] = None,
    filter_description: Optional[str] = None,
) -> Optional[str]:
    """Opens a save dialog. Returns the path or None if canceled."""
    count, c_filters, c_description = _filter_args(filters, filter_description)
    result = tfd.tinyfd_saveFileDialog(
        _c_str(title), _c_str(default_path), count, c_filters, c_description
    )
    return _decode(result)


def open_file_dialog(
    title: str = "Select a file",
    default_path: str = "",
    filters: Optional[list] = None,
    filter_description: Optional[str] = None,
    allow_multiple: bool = False,
) -> Optional[str]:
    """Opens a file picker. Returns the path or None if canceled.
    When allow_multiple is True, multiple paths are separated by '|'.
    """
    count, c_filters, c_description = _filter_args(filters, filter_description)
    result = tfd.tinyfd_openFileDialog(
        _c_str(title), _c_str(default_path), count, c_filters,
        c_description, 1 if allow_multiple else 0
    )
    return _decode(result)


def select_folder_dialog(
    title: str = "Select a folder",
    default_path: str = "",
) -> Optional[str]:
    """Opens a folder picker. Returns the path or None if canceled."""
    result = tfd.tinyfd_selectFolderDialog(
        _c_str(title), _c_str(default_path)
    )
    return _decode(result)


def color_chooser(
    title: str = "Choose a color",
    default_hex_rgb: str = "",
    default_rgb: tuple = (0, 128, 255),
) -> Optional[str]:
    """Opens a color picker. Returns a hex color like '#FF0000' or None."""
    c_default = (ctypes.c_ubyte * 3)(*default_rgb)
    c_result = (ctypes.c_ubyte * 3)()
    result = tfd.tinyfd_colorChooser(
        _c_str(title), _c_str(default_hex_rgb), c_default, c_result
    )
    return _decode(result)


def beep() -> None:
    """Plays the system beep."""
    tfd.tinyfd_beep()
