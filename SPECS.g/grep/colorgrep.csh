
# color-grep initialization

if ( -r /etc/GREP_COLORS ) then
    set color_none=`sed -n '/^COLOR.*none/Ip' < /etc/GREP_COLORS`
    if ( "$color_none" != '' ) then
        unset color_none
        exit
    endif
    unset color_none
endif

alias grep 'grep --color=auto'
alias egrep 'egrep --color=auto'
alias fgrep 'fgrep --color=auto'
