#!/bin/bash
debug=""
#debug="echo"

cd `dirname $0`
LANG=C
SPEC=vim.spec

DATE=`date +"%a %b %d %Y"`
MAJORVERSION=`grep "define baseversion" vim.spec | cut -d ' ' -f 3`
CHLOG="* $DATE Karsten Hopp <karsten@redhat.com> $MAJORVERSION"
ORIGPL=`grep "define patchlevel" vim.spec | cut -d ' ' -f 3 | sed -e "s/^0*//g"`
ORIGPLFILLED=`printf "%03d" $ORIGPL`
PL=$ORIGPL

git pull

while true; do
    LASTPL=$PL
    LASTPLFILLED=`printf "%03d" $LASTPL`
    PL=$((PL+1))
    PLFILLED=`printf "%03d" $PL`
    PNAME="$MAJORVERSION.$PLFILLED"
    URL="ftp://ftp.vim.org/pub/vim/patches/$MAJORVERSION/$PNAME"
    wget -nc $URL 2>/dev/null
    if [ "$?" -ne "0" ]; then
        # Patchlevel not yet available, back down
        PL=$LASTPL
        PLFILLED=$LASTPLFILLED
        LASTPL=$((LASTPL-1))
        LASTPLFILLED=`printf "%03d" $LASTPL`
        if [ "$PL" == "$ORIGPL" ]; then
            echo "No new patchlevel available"
            exit
        fi
        break
    else
        # echo "Got patchlevel $MAJORVERSION.$PL, current CVS is at $MAJORVERSION.$ORIGPL"
        $debug git add $PNAME
        $debug git commit -m "- patchlevel $PLFILLED" $PNAME
        sed -i -e "/Patch$LASTPLFILLED: ftp:\/\/ftp.vim.org\/pub\/vim\/patches\/$MAJORVERSION\/$MAJORVERSION.$LASTPLFILLED/aPatch$PLFILLED: ftp:\/\/ftp.vim.org\/pub\/vim\/patches\/$MAJORVERSION\/$MAJORVERSION.$PLFILLED" $SPEC
        sed -i -e "/patch$LASTPLFILLED -p0/a%patch$PLFILLED -p0" $SPEC
    fi
done
sed -i -e "/Release: /cRelease: 1%{?dist}" $SPEC
sed -i -e "s/define patchlevel $ORIGPLFILLED/define patchlevel $PLFILLED/" $SPEC
sed -i -e "/\%changelog/a$CHLOG.$PLFILLED-1\n- patchlevel $PLFILLED\n" $SPEC
wget ftp://ftp.vim.org/pub/vim/patches/$MAJORVERSION/README -O README.patches
$debug git add vim.spec README.patches
$debug git commit -m "- patchlevel $PL" 
$debug git push
if [ $? -eq 0 ]; then
    $debug rm -f $HOME/.koji/config
    $debug fedpkg build
    $debug ln -sf ppc-config $HOME/.koji/config
else
    echo "GIT push failed"
fi
