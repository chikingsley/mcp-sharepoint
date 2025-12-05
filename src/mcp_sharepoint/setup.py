"""Certificate setup for SharePoint MCP Server."""

import subprocess
import sys
from pathlib import Path


def generate_certificate(output_dir: str = "certs", days: int = 365) -> dict[str, str]:
    """Generate a self-signed certificate for SharePoint authentication.

    Args:
        output_dir: Directory to store certificate files
        days: Certificate validity in days

    Returns:
        Dictionary with cert_path, key_path, pem_path, and thumbprint
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    key_file = output_path / "sharepoint.key"
    crt_file = output_path / "sharepoint.crt"
    pem_file = output_path / "sharepoint.pem"

    # Generate certificate using openssl
    try:
        subprocess.run(
            [
                "openssl",
                "req",
                "-x509",
                "-sha256",
                "-nodes",
                "-days",
                str(days),
                "-newkey",
                "rsa:2048",
                "-keyout",
                str(key_file),
                "-out",
                str(crt_file),
                "-subj",
                "/CN=mcp-sharepoint/O=MCP SharePoint Server",
            ],
            check=True,
            capture_output=True,
        )
    except FileNotFoundError:
        print("Error: openssl not found. Please install OpenSSL.")
        print("  macOS: brew install openssl")
        print("  Ubuntu: sudo apt install openssl")
        print("  Windows: Install from https://slproweb.com/products/Win32OpenSSL.html")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error generating certificate: {e.stderr.decode()}")
        sys.exit(1)

    # Combine into PEM file
    with pem_file.open("w") as pem:
        pem.write(crt_file.read_text())
        pem.write(key_file.read_text())

    # Get thumbprint
    result = subprocess.run(
        ["openssl", "x509", "-in", str(crt_file), "-fingerprint", "-sha1", "-noout"],
        capture_output=True,
        text=True,
        check=True,
    )
    thumbprint = result.stdout.strip().replace("sha1 Fingerprint=", "").replace(":", "")

    return {
        "cert_path": str(crt_file),
        "key_path": str(key_file),
        "pem_path": str(pem_file),
        "thumbprint": thumbprint,
    }


def setup():
    """Interactive setup for SharePoint MCP Server."""
    print("=" * 60)
    print("SharePoint MCP Server - Certificate Setup")
    print("=" * 60)
    print()

    # Generate certificate
    print("Generating self-signed certificate...")
    result = generate_certificate()
    print(f"  Certificate: {result['cert_path']}")
    print(f"  Private key: {result['key_path']}")
    print(f"  Combined PEM: {result['pem_path']}")
    print(f"  Thumbprint: {result['thumbprint']}")
    print()

    # Instructions
    print("=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print()
    print("1. Upload the certificate to Azure:")
    print("   - Go to https://portal.azure.com")
    print("   - Navigate to: App registrations > Your App > Certificates & secrets")
    print("   - Click 'Certificates' tab > 'Upload certificate'")
    print(f"   - Upload: {result['cert_path']}")
    print()
    print("2. Add these to your .env file:")
    print()
    print(f"   SHP_CERT_PATH={result['pem_path']}")
    print(f"   SHP_CERT_THUMBPRINT={result['thumbprint']}")
    print()
    print("3. Make sure you have SharePoint API permissions:")
    print("   - App registrations > Your App > API permissions")
    print("   - Add permission > SharePoint > Application permissions")
    print("   - Select: Sites.FullControl.All (or Sites.ReadWrite.All)")
    print("   - Click 'Grant admin consent'")
    print()
    print("=" * 60)
    print("Setup complete! Run 'mcp-sharepoint' to start the server.")
    print("=" * 60)


if __name__ == "__main__":
    setup()
