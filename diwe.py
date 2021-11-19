#!/usr/bin/env python3

## Run with: nohup ./diwe.py <ARGS> &

## apt install python3-pip
## python3 -m pip install filetype

import sys
import os
import argparse
import time

import filetype


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
    ## mutually exclusive arguments:
    time_mode = parser.add_mutually_exclusive_group()
    time_mode.add_argument(
        "-t",
        "--time",
        type=int,
        default=None,
        help="set time in seconds after which next image will be displayed in dynamic wallpaper (e.g. \"10\", \"60\", \"3600\", ...)")
    time_mode.add_argument(
        "-T",
        "--exact-time",
        type=str,
        default=None,
        help="set specific time, when image should be changed (e.g. 'xx:xx:30' -> every minute at 30 second mark)")

    ## -r = random
    ## -R = true random

    ## pass arguments:
    args = parser.parse_args()


    ## Wallpaper file:
    wallpaper_file = args.wallpaper

    ## Check if wallpaper was provided:
    if wallpaper_file == None:
        print(f"ERROR! No wallpaper was selected! Select wallpaper with '-w <WALLPAPER>'.",
        file=sys.stderr)
        sys.exit(-1)


    ## Time for dynamic wallpaper:
    wallpaper_time = None
    if args.time != None:
        wallpaper_time = args.time
        ## Time in seconds cannot be negative (and 0 is static):
        if wallpaper_time < 0:
            print(f"ERROR. Specified time '{wallpaper_time}' cannot be negative value!",
            file=sys.stderr)
            sys.exit(-1)
        elif wallpaper_time == 0:
            print(f"ERROR. Specified time '{wallpaper_time}' cannot be 0! Use '-s' for static wallpaper.",
            file=sys.stderr)
            sys.exit(-1)
    elif args.exact_time != None:
        wallpaper_time = args.exact_time


    ## Wallpaper modes:
    ## 0 = static (default)
    ## 1 = dynamic
    ## 2 = live
    ## 3 = hybrid
    ## Check wallpaper mode:
    if args.dynamic:
        ## Check if time was provided:
        if wallpaper_time == None:
            print(f"ERROR! No time was specified! Specify wallpaper with options '-t' or '-T'.",
            file=sys.stderr)
            sys.exit(-1)
        else:
            set_dynamic_wallpaper(wallpaper_file, wallpaper_time)
    elif args.live:
        pass
    elif args.hybrid:
        pass
    else:
        ## If time was specified, print warning:
        if wallpaper_time != None:
            print("Warning! Time argument is not used for static wallpaper and will be ignored.",
            file=sys.stderr)

        ## Check if only one wallpaper argument was provided for static wallpaper:
        if len(wallpaper_file[0]) > 1:
            print("ERROR! Static wallpaper can accept only 1 file!",
            file=sys.stderr)
            sys.exit(-1)
        ## Check if wallpaper is file:
        if os.path.isdir(wallpaper_file[0][0]):
            print(f"ERROR! Specified wallpaper '{wallpaper_file[0][0]}' is directory!",
            file=sys.stderr)
            sys.exit(-1)
        elif not os.path.isfile(wallpaper_file[0][0]):
            print(f"ERROR! Specified wallpaper '{wallpaper_file[0][0]}' does not exists!",
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
        print(f"ERROR! Wallpaper could not be set to '{wallpaper_file}'! Exit code ({exit_code}).",
        file=sys.stderr)
        sys.exit(-1)


def set_dynamic_wallpaper(wallpaper_file, wallpaper_time):
    ## Check amount of wallpaper_file arguments,
    ## 1  = directory (all images in dir will be used),
    ## 2+ = image files (all selected image files will be used):
    if len(wallpaper_file[0]) == 1:
        ## If directory was specified in format 'DIR/' or 'DIR/////...', remove last '/' -> 'DIR':
        while wallpaper_file[0][0][-1] == '/':
            wallpaper_file[0][0] = wallpaper_file[0][0][:-1]

        ## Check if directory exists:
        if os.path.isdir(wallpaper_file[0][0]):
            ## Declare list of images, that will be used for dynamic wallpaper:
            wallpaper_dynamic_list = []

            ## Find all files in directory 'wallpaper_file':
            directory_file_list = os.listdir(f"{wallpaper_file[0][0]}")

            ## If file is valid image, add to 'wallpaper_dynamic_list':
            for file_in_directory in directory_file_list:
                if os.path.isdir(wallpaper_file[0][0] + "/" + file_in_directory):
                    print(f"WARNING! File '{wallpaper_file[0][0]}/{file_in_directory}' is a directory! Directory was skipped.",
                    file=sys.stderr)
                elif filetype.is_image(wallpaper_file[0][0] + "/" + file_in_directory):
                    wallpaper_dynamic_list.append(wallpaper_file[0][0] + "/" + file_in_directory)
                else:
                    print(f"WARNING! File '{wallpaper_file[0][0]}/{file_in_directory}' is not valid image! File was skipped.",
                    file=sys.stderr)

            ## Check if too many files were not dropped (at least 2 files are required for dynamic wallapper):
            if len(wallpaper_dynamic_list) < 2:
                print(f"ERROR! Not enough files for dynamic wallpaper ({len(wallpaper_dynamic_list)})! Maybe you want to specify static wallpaper?",
                file=sys.stderr)
                sys.exit(-1)

            ## Sort list with images alphabetically:
            wallpaper_dynamic_list.sort()
            print(f"Debug: {wallpaper_dynamic_list}")

            ## Set dynamic wallpaper according to '-t' option:
            while 1:
                ## If 'wallapper_time' is int -> '-t' option used by user.
                if isinstance(wallpaper_time, int):
                    ## Loop through all images in 'wallpaper_dynamic_list':
                    for image in wallpaper_dynamic_list:
                        exit_code = os.system(f"feh --bg-scale {image}")
                        if exit_code == 0:
                            print(f"Wallpaper was set to '{image}'.")
                        else:
                            print(f"ERROR! Wallpaper could not be set to '{image}'!",
                            file=sys.stderr)
                        time.sleep(wallpaper_time)

                ## Set dynamic wallpaper accorting to '-T' option:
                elif isinstance(wallpaper_time, str):
                    print("Debug: -T")
                    pass


        elif os.path.isfile(wallpaper_file[0][0]):
            print(f"ERROR! Specified file '{wallpaper_file[0][0]}' is not adirectory but a regular file! Select 1 directory or multiple image files for dynamic wallpaper.",
            file=sys.stderr)
            sys.exit(-1)
        else:
            print(f"ERROR! Specified file '{wallpaper_file[0][0]}' does not exists!",
            file=sys.stderr)
            sys.exit(-1)



"""
            ## Fork gets pid of 0:
            fpid = os.fork()
            if fpid!=0:
                ## Running as daemon now. PID is fpid
                while 1:
                    print("a")
                    time.sleep(5)
            else:
                ## Destroy parent:
                print("Parent closed")
                sys.exit(0)
"""







main()
