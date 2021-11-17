#!/usr/bin/env python3

import sys
import os
import argparse

def main():
    ## create ArgumentParser object and add description of program:
    parser = argparse.ArgumentParser(
        description="Sets wallpaper for GNU/Linux.")

    ## mutually exclusive arguments:
    wallpaper_mode = parser.add_mutually_exclusive_group()
    wallpaper_mode.add_argument(
        "-s",
        "--static",
        action="store_true",
        default=True,
        help="Set static wallpaper"
    )
    wallpaper_mode.add_argument(
        "-d",
        "--dynamic",
        action="store_true",
        default=False,
        help="Set dynamic wallpaper"
    )
    wallpaper_mode.add_argument(
        "-l",
        "--live",
        action="store_true",
        default=False,
        help="Set live wallpaper"
    )
    wallpaper_mode.add_argument(
        "-x",
        "--hybrid",
        action="store_true",
        default=False,
        help="Set hybrid wallpaper"
    )
    ## wallpaper argument:
    parser.add_argument(
        "-w",
        "--wallpaper",
        type=str,
        default=None,
        help="set file as wallpaper")
    ## time arguemnt (for dynamic wallpaper):
    parser.add_argument(
        "-t",
        "--time",
        type=str,
        default=None,
        help="set time for dynamic wallpaper (e.g. \"10\", \"60s\", \"5m\", \"3h\")")

    ## pass arguments:
    args = parser.parse_args()


    ## Wallpaper file:
    wallpaper_file = args.wallpaper

    ## Check if wallpaper was provided:
    if wallpaper_file == None:
        print(f"ERROR! No wallpaper was selected. Select wallpaper with '-w <WALLPAPER>'.",
        file=sys.stderr)


    ## Wallpaper modes:
    ## 0 = static (default)
    ## 1 = dynamic
    ## 2 = live
    ## 3 = hybrid

    ## Check wallpaper mode:
    if args.dynamic:
        pass
    elif args.live:
        pass
    elif args.hybrid:
        pass
    else:
        ## Check if wallpaper is file:
        if os.path.isfile(wallpaper_file):
            set_static_wallpaper(wallpaper_file)
        elif os.path.isdir(wallpaper_file):
            print(f"ERROR! Specified wallpaper '{wallpaper_file}' is directory!",
            file=sys.stderr)
        else:
            print(f"ERROR! Specified wallpaper '{wallpaper_file}' does not exists!",
            file=sys.stderr)


def set_static_wallpaper(wallpaper_file):
    ## Set wallpaper using 'feh':
    exit_code = os.system(f'feh --bg-scale {wallpaper_file}')

    ## Check if command was executed successfully (returned 0):
    if exit_code == 0:
        print(f"Wallpaper was set to '{wallpaper_file}'.")
    else:
        print(f"ERROR! Wallpaper could not be set to '{wallpaper_file}'. Exit code ({exit_code})!",
        file=sys.stderr)


def set_dynamic_wallpaper()
    """
    Parameters = image_list + time
    """
    pass


main()
