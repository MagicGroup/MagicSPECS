## http://kde.ground.cz/tiki-index.php?page=Environment+Variables
## for possible entries here

## Make sure KDEDIRS is set
if ( ! $?KDEDIRS ) setenv KDEDIRS /opt/kde4

## When/if using prelinking, avoids use of kdeinit
## disabled, for now, due to http://bugzilla.redhat.com/515539
#if ( -f /etc/sysconfig/prelink ) then
#   set PRELINKING = `grep "^PRELINKING=" /etc/sysconfig/prelink | cut -d"=" -f2`
#   if ( "$PRELINKING" == "yes" )  then
#     if ( ! $?KDE_IS_PRELINKED ) setenv KDE_IS_PRELINKED 1
#   endif
#   unset PRELINKING
#endif
