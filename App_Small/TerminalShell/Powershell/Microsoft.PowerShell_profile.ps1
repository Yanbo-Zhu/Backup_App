#------------------------------- Import Modules BEGIN -------------------------------
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\unicorn.omp.json" | Invoke-Expression

# 引入 posh-git
Import-Module posh-git

# 引入 ps-read-line
Import-Module PSReadLine

Import-Module -Name Terminal-Icons

# Import zlua
Invoke-Expression (& { (lua d:\SmallApp\Terminal_Programmierung\zlua\z.lua --init powershell) -join "`n" })


#------------------------------- Import Modules END   -------------------------------

#-------------------------------  Set Zlua BEGIN  -------------------------------

$_ZL_MATCH_MODE=1
$_ZL_MAXAGE=2000
$_ZL_HYPHEN=1
$_ZL_ECHO=1

function zl{
    z -l $args
}

function zt{
    z -t $args
}

function zti{
    z -t -i $args
}

function zi{
    z -i $args
}

function zc{
    z -c $args
}

function zb{
    z -b $args
}

function zbi{
    z -b -i $args
}

function zf{
    z -I $args
}

function zft{
    z -I -t $args
}

#-------------------------------  Set Zlua End -------------------------------


#-------------------------------  Set Hot-keys BEGIN  -------------------------------
# 设置预测文本来源为历史记录
Set-PSReadLineOption -PredictionSource History

# 每次回溯输入历史，光标定位于输入内容末尾
Set-PSReadLineOption -HistorySearchCursorMovesToEnd

#
Set-PSReadlineOption -MaximumHistoryCount 10000

# 设置 Tab 为菜单补全和 Intellisense
Set-PSReadLineKeyHandler -Key "Tab" -Function MenuComplete

# 设置 Ctrl+d 为退出 PowerShell
Set-PSReadlineKeyHandler -Key "Ctrl+d" -Function ViExit

# 设置 Ctrl+z 为撤销
Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo

# 设置向上键为后向搜索历史记录
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward

# 设置向下键为前向搜索历史纪录
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward


#-------------------------------  Set Hot-keys END    -------------------------------

#-------------------------------   Set Alias BEGIN    -------------------------------

# 3. 查看目录 ls & ll
function ListDirectory {
	(Get-ChildItem).Name
	Write-Host("")
}
Set-Alias -Name ls -Value ListDirectory
Set-Alias -Name ll -Value Get-ChildItem

# 4. 打开当前工作目录
function OpenCurrentFolder {
	param
	(
		# 输入要打开的路径
		# 用法示例：open C:\
		# 默认路径：当前工作文件夹
		$Path = '.'
	)
	Invoke-Item $Path
}
Set-Alias -Name open -Value OpenCurrentFolder
#-------------------------------    Set Alias END     -------------------------------

