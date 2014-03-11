############################################################ fbsplash
if [ -f /sbin/splash-functions.sh ]; then
      . /sbin/splash-functions.sh
fi

# Exit fbsplashd
fbsplash_exit()
{
splash critical
splash svc_stop
splash rc_exit 
}

# Start fbsplash in sysinit
fbsplash_boot()
{
splash rc_init sysinit
}

# Start fbsplash in rc script
fbsplash_rc()
{
splash rc_init
}

# Stop fbsplashd
fbsplash_shutdown()
{
splash svc_stop
}

# Stop fbsplashd
fbsplash_stop()
{
splash critical
splash_comm_send "exit"
splash_cache_cleanup
}

fbsplash_check_exit()
{
pidof fbsplash.static >/dev/null && splash_stop
}

# Set fbsplash Progressbar and draw .
# progress is 1 to 65535 , NOT 1 TO 100 !
progressbar()
{
progress=$1
splash_update_progress
}

fbsplash_set_tty()
{
if [ -z ${SPLASH_SET_TTYS} ]; then
	SPLASH_SET_TTYS="1 2 3 4 5 6"
fi

for x in ${SPLASH_SET_TTYS}
do
	fbcondecor_set_theme ${SPLASH_THEME} ${x}
done
}
