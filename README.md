color-eva
=========

Simple CLI to send a color code to EVA painter and save the JSON output.

Quick run (from this folder without installing):

```bash
python color-eva.py generate "#9D2A28"
```

Install (creates `color-eva` command when installed):

```bash
pip install -e .
color-eva generate "#9D2A28"
```

Output
- Saves JSON to your Downloads folder as `color-eva-generate-9D2A28.json` (hex code without `#`).

Options
- `--retries N`: number of retries on network failure (default: 2)
- `--timeout N`: request timeout seconds (default: 30)
- `--backoff N`: base backoff seconds for exponential backoff (default: 1.0)
- `-v, --verbose`: enable verbose debug output
- `-o, --out`: specify output file path
- `--open`: open the saved file after writing

Examples

```bash
python color-eva.py generate "#9D2A28" -v --retries 3 --timeout 10 --out ./color-eva-test.json
```

Notes
- The CLI sends a GET request to the EVA painter endpoint with the `color` query parameter (hex, without `#`).
- Short hex codes like `#F0A` are expanded to `#FF00AA`.

Output format (updated)
- The saved JSON is now converted into an array with a single object where each key is a named token like `color-<group>-<scale>` and the value is an array of `["#HEX", "rgb(r, g, b)"]`.

Example (partial):

```json
[
	{
		"color-primary-100": ["#DDE7FA", "rgb(221, 231, 250)"],
		"color-primary-200": ["#BCCFF6", "rgb(188, 207, 246)"],
		"color-primary-300": ["#94ACE6", "rgb(148, 172, 230)"]
	}
]
```

If you prefer the previous raw API structure, tell me and I can add a `--raw` flag to keep the original response.

Make `color-eva` available globally
----------------------------------

1) Recommended — add Python `Scripts` folder to your user PATH (one-time):

Run the helper included in this repo (no admin required):

```powershell
cd <path-to-this-repo>
install-global.bat
```

After that, close and re-open Command Prompt or PowerShell, then run:

```powershell
color-eva --help
```

2) Manual alternative — find the scripts folder and add to PATH yourself:

```powershell
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
setx PATH "%PATH%;C:\path\to\that\Scripts"
```

If `color-eva` is still not found, run the tool with:

```powershell
python -m color_eva.cli generate "#9D2A28"
```

