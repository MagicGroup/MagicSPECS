## http://kde.ground.cz/tiki-index.php?page=Environment+Variables
## for possible entries here

## Make sure KDEDIRS is set
[ -z "$KDEDIRS" ] && KDEDIRS="/opt/kde4" && export KDEDIRS

## When/if using prelinking, avoids (some) use of kdeinit
## disabled, for now, due to http://bugzilla.redhat.com/515539
#if [ -z "$KDE_IS_PRELINKED" ] ; then
#  grep -qs '^PRELINKING=yes' /etc/sysconfig/prelink && \
#  KDE_IS_PRELINKED=1 && export KDE_IS_PRELINKED
#fi
