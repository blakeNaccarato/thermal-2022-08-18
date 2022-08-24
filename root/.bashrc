#!/bin/bash

#! ---------------------------------------------------------------------------------- !#
#! TRICK/GUNNS

export GUNNS_EXT_PATH=""
export GUNNS_HOME="/home/gunns"

#! ---------------------------------------------------------------------------------- !#
#! DOCKER

export DISPLAY=host.docker.internal:0.0

#! ---------------------------------------------------------------------------------- !#
#! ENVIRONMENT

#* Trim the display of parent directories in the prompt
PROMPT_DIRTRIM=2

#* Import dotenv aka .env environment variables if it is found
if [ -f ./.env ] ; then
    set -o allexport # enable shell option to export all created variables
    source ./.env # now this will export all vars instead of just one
    set +o allexport # disable shell option to export all created variables
fi

#* Activate virtual environment if a .venv folder is detected
if [ -d .venv ] ; then
    source .venv/bin/activate
fi

#! ---------------------------------------------------------------------------------- !#
#! UBUNTU BASHRC

# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

#! ---------------------------------------------------------------------------------- !#
#! NASA GUNNS BASHRC

# Copyright 2019 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration.  All Rights Reserved.
#
# Usage: . bashrc (source this file)
# This bashrc is designed to produce a bash environment that fully emulates the environment
# created by the cshrc that lives alongside it.  With this design, any changes to environment
# can be made to the cshrc, and they will automatically be applied to bash environments
#
# Limitations: the ? is used as a delimeter, which means if theres a ? anywhere in the env
# something is going to go wrong.  I tried multi-character delimiters (,,) but it still seemed
# to split on single ,'s. If multicharacter delims would work this problem would go away
#

# Ensure variables to be used are empty
unset bashExportLines;
unset fullTcshEnv;
unset allOneLine;
unset ADDR;

# Global env exclusion list -- these will be not absorbed from tcsh env
included=1;
excludeList[0]='module=';
excludeList[1]='DISPLAY';
excludeList[2]='TERM';
excludeList[3]='^HOME=';
excludeList[4]='.*SSH.*';
excludeList[5]='SHELL';
excludeList[6]='WINDOWID';
excludeList[7]='LS_COLORS';
excludeList[8]='GNOME_KEYRING_SOCKET';
excludeList[9]='DESKTOP_SESSION';
excludeList[10]='^MAIL=';
excludeList[11]='^PWD=';
excludeList[12]='^DBUS_SESSION_BUS_ADDRESS=';
excludeList[13]='^guid=';
excludeList[14]='^MODULES_HOME=';
excludeList[15]='^BASH_FUNC_module';


# This function sets included to be true if the argument
# passed does not contain any regular expressions stored in
# the excludList array
function isNotInExcludeList {
    included=1
    for reg in "${excludeList[@]}"; do
       if [[ $1 =~ $reg ]]; then
           #echo "excluded!"
           included=0
           break
       fi
    done
}

#! Modified
# Get the full environment from a tcsh shell that sourced the cshrc, then
# add quotes to the env lines so that var=bleh blah becomes var="bleh blah"
# and replace every line ending with a ? as a delimeter
fullTcshEnv=`tcsh -f  -c "source /root/.cshrc $@; env | sed 's/=/=\"/' | sed 's/$/\"?/'"`;

# Collapse newlines to make all variables on one line
#echo "$fullTcshEnv"
allOneLine=`echo $fullTcshEnv`
#echo "alloneline $allOneLine"

# Split environment by newline and match to VAR= form
# Then store the variable as an export line to be executed later
regex="^ *[a-zA-Z].*="
# Turn off fileglobbing, to preserve * characters
set -f
IFS='?' read -ra ADDR <<< "$allOneLine"
j=0
for line in "${ADDR[@]}"; do
   #echo "line is $line"
   # Check to see if this variable is in exclude list
   isNotInExcludeList $line
   #echo "included is $included"
   #echo "line is $line"
   #echo "regex is $regex"
   if [[ $line =~ $regex ]]; then
       if [[ $included == 1 ]]; then
          #echo "STORING line $line"
          bashExportLines[j]="export $line"
          j=`expr $j + 1`
       fi
   fi

done
unset IFS

# Now bashExportLines contains every 'export VAR="value"' line we need
# just eval each line and walk away in slow motion like a boss
for line in "${bashExportLines[@]}"; do
   #echo "Evaling $line"
   eval $line
done

# Turn  fileglobbing back on
set +o noglob
