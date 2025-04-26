from pathlib import Path
import subprocess
import tempfile
from fastapi import FastAPI, UploadFile, Request


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Basic fastapi setup with /invert/ endpoint
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def temp_dir() -> Path:
    """Create a temporary directory for the PDF files."""
    temp_dir = Path(tempfile.gettempdir())
    if not temp_dir.is_dir():
        raise ValueError(f"Temp dir {temp_dir} is not a directory.")
    return temp_dir


def gs_invert(input_path: Path) -> Path:
    """Inverts the colors of a PDF file using Ghostscript."""
    output_path = input_path.with_stem(input_path.stem + ".inverted")
    gs_command = [
        "gs",
        "-o",
        str(output_path),
        "-sDEVICE=pdfwrite",
        "-dPDFUseOldCMS=false",
        "-dBATCH",
        "-dNOPAUSE",
        "-sProcessColorModel=DeviceRGB",
        "-sColorConversionStrategy=LeaveColorUnchanged",
        "-dCompatibilityLevel=1.4",
        "-c",
        "<< /Install { {1 exch sub} settransfer } >> setpagedevice",
        "-f",
        str(input_path),
    ]
    subprocess.run(gs_command, check=True)
    return output_path


"""FastAPI endpoint, /invert, which takes PDF data and downloads it to local disk."""


@app.post("/invert")
async def invert(request: Request) -> FileResponse:
    """FastAPI endpoint, /invert, which takes PDF data and downloads it to local disk."""
    data = await request.form()
    if "file" not in data:
        raise ValueError("No file found in the request.")
    data = data["file"]
    print(f"Received file: {data}")
    local_file = temp_dir() / data.filename
    local_file.unlink(missing_ok=True)
    local_file.touch()
    handle = local_file.open("wb")
    handle.write(data.file.read())
    handle.close()

    # Invert the PDF file using Ghostscript
    inverted_file = gs_invert(local_file)

    # Remove the original file
    local_file.unlink(missing_ok=True)

    return FileResponse(
        inverted_file,
        media_type="application/pdf",
        filename=inverted_file.name,
    )
