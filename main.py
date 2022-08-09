import subprocess
import sys
from src.tikdown import *

list_downloaded = []


def run_process_windows():
    from win10toast_click import ToastNotifier
    import time

    toaster = ToastNotifier()

    if pyperclip.paste() in list_downloaded:
        pass
    else:

        tikdownload = tikdown()
        if "tiktok" in pyperclip.paste():

            if tikdownload.get_id_video(pyperclip.paste()):

                if tikdownload.download_no_watermark():
                    list_downloaded.append(pyperclip.paste())
                    print("Downloaded: " + tikdownload.nick_name + " - " + tikdownload.vid_id)
                    toaster.show_toast(
                        title="TikClick",
                        msg="Downloaded " + tikdownload.nick_name + "'s video Click to open",
                        duration=0.1,
                        icon_path=os.getcwd() + "/src/icon.ico",
                        callback_on_click=lambda: os.startfile(
                            os.getcwd() + "/downloads/" + tikdownload.nick_name + "/" + tikdownload.vid_id + ".mp4")
                    )

                    while toaster.notification_active():
                        time.sleep(0)
                else:
                    toaster.show_toast(
                        title="Tiktok Downloader",
                        msg="Video not found",
                        duration=5,
                        icon_path=os.getcwd() + "/src/icon.ico"
                    )
            else:
                pass

        else:
            pass


def run_process_linux(argv):
    # !/usr/bin/env python3
    import subprocess

    if pyperclip.paste() in list_downloaded:
        pass
    else:

        tikdownload = tikdown()
        if "tiktok" in pyperclip.paste():

            if tikdownload.get_id_video(pyperclip.paste()):

                if tikdownload.download_no_watermark():
                    list_downloaded.append(pyperclip.paste())
                    print("Downloaded: " + tikdownload.nick_name + " - " + tikdownload.vid_id)
                    subprocess.call(
                        ["notify-send", "TikClick", "Downloaded " + tikdownload.nick_name + "'s video"])

                    if argv.upper() == "TRUE":
                        subprocess.call(["xdg-open",
                                         os.getcwd() + "/downloads/" + tikdownload.nick_name + "/" + tikdownload.vid_id + ".mp4"])
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass


if __name__ == '__main__':
    try:
        # check installed module and install if not installed
        try:
            import pyperclip
        except ImportError:
            subprocess.call(["pip3", "install", "pyperclip"])
            print("[!] pyperclip installed")

        try:
            import requests
        except ImportError:
            subprocess.call(["pip3", "install", "requests"])
            print("[!] requests installed")

        if sys.platform == "win32":

            try:
                import win10toast_click
            except ImportError:
                subprocess.call(["pip3", "install", "win10toast_click"])
                print("[!] win10toast_click installed")

            from win10toast_click import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                title="Tiktok Downloader",
                msg="Welcome to TikClick, You can download TikTok videos without watermark",
                duration=5,
                icon_path=os.getcwd() + "/src/icon.ico"
            )


        elif sys.platform == "linux":

            if subprocess.call(["which", "notify-osd"]) == 1:
                pass
            else:
                subprocess.call(["sudo", "apt-get", "install", "notify-osd"], shell=False, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
                print("[!] notify-send installed")

            if subprocess.call(["which", "xclip"]) == 1:
                pass

            else:
                subprocess.call(["sudo", "apt-get", "install", "xclip"], shell=False, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
                print("[!] xclip installed")

            subprocess.call(
                ["notify-send", "TikClick", "Welcome to TikClick, You can download TikTok videos without watermark"])

        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--auto_show", help="Auto open video after download (True/False)", required=True)
        args = parser.parse_args()

        if args.auto_show.upper() == "TRUE":
            pass
        elif args.auto_show.upper() == "FALSE":
            pass
        else:
            print("Error: --auto_show must be True or False")
            sys.exit()

        while True:
            if sys.platform == "win32":
                run_process_windows()
            elif sys.platform == "linux":
                run_process_linux(argv=args.auto_show)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()
