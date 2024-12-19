:: Setup for window - will be removed at some point
@echo off

:: Base package root. Change it for your directory
set ASTROFIX_ROOT=C:\Users\sgro\work\AstroPix\astrofix

:: This is were i store data
set ASTROFIX_DATA=C:\Users\sgro\work\AstroPix\astropix-outdata

:: AstroPix library package root. Change it for your directory
set ASTROPIX_ROOT=C:\Users\sgro\work\AstroPix\astropix-python

:: Add the root folder to the $PYTHONPATH to import  the relevant modules.
set PYTHONPATH=%ASTROFIX_ROOT%;%ASTROPIX_ROOT%
