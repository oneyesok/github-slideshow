# Cursor 快捷命令
alias c='cursor'                    # 快速打开 cursor
alias cw='cursor serve-web &'       # 启动 web 模式
alias co='cursor .'                 # 在当前目录打开
alias cg='cursor -g'                # 快速跳转到指定行
alias cd='cursor --diff'            # 文件比较
alias cwa='cursor --wait'           # 等待模式

# AI 分析快捷命令
alias analyze='cursor -'            # 管道分析
alias gitai='git diff | cursor -'   # Git diff AI 分析
alias logai='tail -f /var/log/system.log | cursor -'  # 日志AI分析

# 实用函数
copen() {
    if [ $# -eq 0 ]; then
        cursor .
    else
        cursor "$@"
    fi
}

# 智能文件查找并打开
cfind() {
    find . -name "*$1*" -type f | head -10 | xargs cursor
}

# 项目快速切换
cproject() {
    cd ~/Projects/$1 && cursor .
}