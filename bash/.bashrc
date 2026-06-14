#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

EDITOR=nvim
VISUAL=nvim

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias la='ls -la'
alias vi='nvim'
alias vim='nvim'

PROMPT_COMMAND='
branch=$(git branch --show-current 2>/dev/null)
PS1_CMD1="$branch"
'

PS1='\[\e[38;5;75m\]\u\[\e[0m\] \
\[\e[38;5;113m\]\w\[\e[0m\]\
${PS1_CMD1:+ \[\e[38;5;242m\]${PS1_CMD1}\[\e[0m\]} \$ '

eval "$(zoxide init bash --cmd cd)"

alias xclip='xclip -selection clipboard'

HISTTIMEFORMAT="%d/%m/%y %T "

export JAVA_HOME="/usr/lib/jvm/java-21-openjdk/"
export PATH=$PATH:$JAVA_HOME/bin
