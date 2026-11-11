# pytinyfiledialogs

Native OS dialogs for Python: message box, file open and save, folder picker,
input box, color chooser, notification, and beep.

No Qt. No Tk. No GUI toolkit. It is a thin `ctypes` wrapper around
[tinyfiledialogs](http://tinyfiledialogs.sourceforge.net) v3.22.1, so the
dialogs look like your system dialogs on Linux, macOS, and Windows.

## Install

```bash
pip install pytinyfiledialogs
```

The wheel contains the compiled library for all three platforms. The right one
is picked at import time.

Python 3.8 or newer.

## Usage

```python
import pytinyfiledialogs as tfd
```

| Function | Returns |
|---|---|
| `message_box(title, message, dialog_type="ok", icon_type="info")` | `1` yes/ok, `0` no or cancel, `2` no in `yesnocancel` |
| `notify_popup(title, message, icon_type="info")` | `1` |
| `input_box(title, message, default_input="")` | text, or `None` on cancel |
| `open_file_dialog(title, default_path="", filters=None, filter_description=None, allow_multiple=False)` | path, or `None` on cancel |
| `save_file_dialog(title, default_path="", filters=None, filter_description=None)` | path, or `None` on cancel |
| `select_folder_dialog(title, default_path="")` | path, or `None` on cancel |
| `color_chooser(title, default_hex_rgb="", default_rgb=(0, 128, 255))` | `"#RRGGBB"`, or `None` on cancel |
| `beep()` | nothing |

`dialog_type` is one of `ok`, `okcancel`, `yesno`, `yesnocancel`.
`icon_type` is one of `info`, `warning`, `error`, `question`.

### Pick a file

```python
path = tfd.open_file_dialog(
    title="Pick an image",
    filters=["*.png", "*.jpg"],
    filter_description="Images",
)
print(path)  # "/home/me/cat.png", or None
```

With `allow_multiple=True`, the returned paths are joined with `|`:

```python
paths = tfd.open_file_dialog(filters=["*.txt"], allow_multiple=True)
for path in (paths or "").split("|"):
    ...
```

### Ask for text

```python
name = tfd.input_box("Your name", "Type it below")

# default_input=None gives a password box (characters are hidden)
password = tfd.input_box("Password", "", default_input=None)
```

### Save a file

```python
path = tfd.save_file_dialog(
    title="Save report",
    default_path="report.txt",
    filters=["*.txt"],
    filter_description="Text files",
)
```

## Notes

- **Filters are glob patterns**, like `*.png`, not descriptions. They only
  control which files the dialog shows. They are not a security check.
- **Quotes are rejected.** The C library refuses `"` in titles and filter
  descriptions. Avoid them, or the dialog shows an error text instead.
- **Linux needs a dialog backend.** Install `zenity` or `kdialog`. Without one,
  the library falls back to a terminal prompt or a plain input prompt.
- **`yesnocancel` uses three numbers.** `1` is Yes, `2` is No, `0` is Cancel.
  In a two-button box, No is `0` instead.
- **macOS and Windows need nothing extra.** They use native dialogs.

## Build from source

Needed for local development. `make` builds only the library for your own OS.

```bash
git clone https://github.com/ippokrates/pytinyfiledialogs
cd pytinyfiledialogs
make
python3 -c "import pytinyfiledialogs as t; print(t.tfd.tinyfd_messageBox)"
```

The release wheel needs Linux, macOS, and Windows binaries, so it is built by
GitHub Actions, not locally.

## Releasing

`pyproject.toml` and the tag must match: `version = "1.0.0"` and `v1.0.0`.

```bash
git tag v1.0.0
git push origin v1.0.0
```

That starts the workflow. It builds all three binaries, makes one wheel, and
creates the GitHub Release with the wheel attached.

Do not click "Draft a new release" on GitHub. The workflow creates the release,
and a second one fails with "release already exists".

## License

Zlib. See [LICENSE](LICENSE).

Built on tinyfiledialogs v3.22.1 by Guillaume Vareille, also under the Zlib
license.
