from pathlib import Path

import click
import qrcode

_default_save_path = str(Path.home() / "Documents")


@click.command()
@click.option("--ssid", "-s", "ssid", required=True, help="Name of the network (SSID)")
@click.option(
    "--password", "-p", "password", required=True, help="Password of the network"
)
@click.option(
    "--path",
    default=_default_save_path,
    show_default=True,
    type=click.Path(exists=True),
    help="Path where the qr code is saved to (Use `--path .` for current working directory).",
)
def gen_wifi_qr(ssid, password, path):
    """
    Creating a QR code based on an SSID and credentials of a wifi network.
    """

    # Creates a .png containg the wifi network's credentials, by default it is saved to ~/Downloads.\n
    # Refer to https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11.\n
    # Layout of the string (as of 2022-03-08) is WIFI:T:WPA;S:mynetwork;P:mypass;;

    click.echo(str(path))

    if path != _default_save_path:
        if path == ".":
            save_path = str(Path.cwd())
        else:
            save_path = path
    else:
        save_path = _default_save_path

    wifi_string = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    img = qrcode.make(wifi_string)
    img.save(f"{save_path}/wifi_{ssid}.png")

    click.echo(f"Generated QR code for {ssid}!")
    click.echo(f"Saving it to {save_path}")


if __name__ == "__main__":
    gen_wifi_qr()
