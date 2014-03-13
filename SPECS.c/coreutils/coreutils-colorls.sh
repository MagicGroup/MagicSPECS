# color-ls initialization

# Skip all for noninteractive shells.
[ -z "$PS1" ] && return

#when USER_LS_COLORS defined do not override user LS_COLORS, but use them.
if [ -z "$USER_LS_COLORS" ]; then

  alias ll='ls -l' 2>/dev/null
  alias l.='ls -d .*' 2>/dev/null

  INCLUDE=
  COLORS=

  for colors in "$HOME/.dir_colors.$TERM" "$HOME/.dircolors.$TERM" \
      "$HOME/.dir_colors" "$HOME/.dircolors"; do
    [ -e "$colors" ] && COLORS="$colors" && \
    INCLUDE="`cat "$COLORS" | grep '^INCLUDE' | cut -d ' ' -f2-`" && \
    break
  done

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS.$TERM" ] && \
  COLORS="/etc/DIR_COLORS.$TERM"

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS.256color" ] && \
  [ "x`tty -s && tput colors 2>/dev/null`" = "x256" ] && \
  COLORS="/etc/DIR_COLORS.256color"

  [ -z "$COLORS" ] && [ -e "/etc/DIR_COLORS" ] && \
  COLORS="/etc/DIR_COLORS"

  # Existence of $COLORS already checked above.
  [ -n "$COLORS" ] || return

  TMP="`mktemp .colorlsXXX --tmpdir=/tmp`"

  [ -e "$INCLUDE" ] && cat "$INCLUDE" >> $TMP
  grep -v '^INCLUDE' "$COLORS" >> $TMP

  eval "`dircolors --sh $TMP 2>/dev/null`"

  rm -f $TMP

  [ -z "$LS_COLORS" ] && return
  grep -qi "^COLOR.*none" $COLORS >/dev/null 2>/dev/null && return
fi

unset TMP COLORS INCLUDE

alias ll='ls -l --color=auto' 2>/dev/null
alias l.='ls -d .* --color=auto' 2>/dev/null
alias ls='ls --color=auto' 2>/dev/null
