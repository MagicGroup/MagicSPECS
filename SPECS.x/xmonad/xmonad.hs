-- default desktop configuration for Fedora

import System.Posix.Env (getEnv, putEnv)
import Data.Maybe (maybe)

import XMonad
import XMonad.Config.Desktop
import XMonad.Config.Gnome
import XMonad.Config.Kde
import XMonad.Config.Xfce

main = do
     session <- getEnv "DESKTOP_SESSION"
     putEnv "_JAVA_AWT_WM_NONREPARENTING=1"
     xmonad  $ maybe desktopConfig desktop session

desktop "gnome" = gnomeConfig
desktop "kde" = kde4Config
desktop "xfce" = xfceConfig
desktop "xmonad-mate" = gnomeConfig
desktop _ = desktopConfig
