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
    ## wallpaper argument [['ARG1', 'ARG2', ...]]:
    parser.add_argument(
        "-w",
        "--wallpaper",
        type=str,
        default=None,
        action='append',
        nargs='+',
        help="set file as wallpaper")
    ## time argument (for dynamic wallpaper):
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
        sys.exit(-1)


    ## Time for dynamic wallpaper:
    wallpaper_time = args.time


    ## Wallpaper modes:
    ## 0 = static (default)
    ## 1 = dynamic
    ## 2 = live
    ## 3 = hybrid

    ## Check wallpaper mode:
    if args.dynamic:
        pass
       ## Check if time was provided:
        if wallpaper_time == None:
            print(f"ERROR! No time was specified! Specify wallpaper with '-t <TIME>'.",
            file=sys.stderr)
            sys.exit(-1)
        else:
            set_dynamic_wallpaper(wallpaper_file, wallpaper_time)
    elif args.live:
        pass
    elif args.hybrid:
        pass
    else:
        ## Check if only one wallpaper argument was provided for static wallpaper:
        if len(wallpaper_file[0]) > 1:
            print("ERROR! Static wallpaper can accept only 1 file.")
            sys.exit(-1)
        ## Check if wallpaper is file:
        if not os.path.isfile(wallpaper_file[0][0]):
            print(f"ERROR! Specified wallpaper '{wallpaper_file[0][0]}' does not exists!",
            file=sys.stderr)
            sys.exit(-1)
        elif os.path.isdir(wallpaper_file[0][0]):
            print(f"ERROR! Specified wallpaper '{wallpaper_file[0][0]}' is directory!",
            file=sys.stderr)
            sys.exit(-1)
        else:
            set_static_wallpaper(wallpaper_file[0][0])


def set_static_wallpaper(wallpaper_file):
    ## Set wallpaper using 'feh':
    exit_code = os.system(f'feh --bg-scale {wallpaper_file}')

    ## Check if command was executed successfully (returned 0):
    if exit_code == 0:
        print(f"Wallpaper was set to '{wallpaper_file}'.")
        sys.exit(0)
    else:
        print(f"ERROR! Wallpaper could not be set to '{wallpaper_file}'. Exit code ({exit_code})!",
        file=sys.stderr)
        sys.exit(-1)


def set_dynamic_wallpaper(wallpaper_file, wallpaper_time):
    ## Check amount of wallpaper_file arguments,
    ## 1  = directory (all images in dir will be used),
    ## 2+ = image files (all selected image files will be used):
    if len(wallpaper_file[0]) == 1:
        ## Find all images in directory:
        pass
    else:
        ## Use all arguments as wallpaper images:
        pass


main()
