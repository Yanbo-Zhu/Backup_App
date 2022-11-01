import argparse
# from git import rmtree
import sys, os, shutil, errno, stat
import logging
import git
from os import path
from time import gmtime, strftime

### constant variable
time_format = "%Y-%m-%d_%H:%M:%S"


### Function
def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Run Ranorex Solution. Display the Debug Information to console in realtime as well as redirect it into a text file simultaneously ",
                                     epilog="Example1: %(prog)s d:\RuntimeTestFPL\\bin\Debug\RuntimeTestFPL.exe -w \n" +
                                            "Example2: %(prog)s d:\RuntimeTestFPL\\bin\Debug\RuntimeTestFPL.exe -a -l r:\yzh\Ranorex\LogFile.txt"
                                     )
    parser.add_argument("pathToTestExecutableOfRanorexSolution", metavar='path_to_Test_Executable', type=str,
                        help="Absolute Path To Test Executable of a Ranorex Solution")
    parser.add_argument("-l", "--pathToLogFile", metavar='path_to_Log_File', type=str,
                        help="Absolute Path To log file. If this Argument is not given, A new log file (.txt) will be created in %%USERPROFILE%%/Desktop")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-w", "--write", action="store_true",
                       help="The Debug Information will be overwritten into file")
    group.add_argument("-a", "--append", action="store_true",
                       help="The Debug Information will be appended into the end of file")

    return parser.parse_args(args)


def copyFileToFile(source_path: str, target_path: str):
    '''
    :param source_path: like C:\hello.txt
    :param target_path: like C:\myweb\chapter02\hello.txt
    :return: no return
    '''

    if os.path.exists(target_path):  # 如果目标路径存在文件的话，就删除它
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        os.unlink(target_path)

    # copy the file into a directory
    shutil.copy(source_path, target_path)

    print('Copy files finished!: ' + source_path + '  to  ' + target_path)


def copyFileToDir(source_path: str, source_filename: str, target_path_root: str):
    '''
    :param source_path: like C:\hello.txt
    :param source_filename: like hello.txt
    :param target_path_root: C:\myweb\chapter02
    :return: Null
    '''

    if not os.path.exists(target_path_root):  # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path_root)

    target_path = os.path.join(target_path_root, source_filename)
    if os.path.exists(target_path):  # 如果目标路径存在文件的话，就删除它
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        os.unlink(target_path)

    # copy the file into a directory
    shutil.copy(source_path, target_path)

    print('Copy files finished!: ' + source_path + '  to  ' + target_path)


def copyDirToDir(source_path: str, target_path: str):
    '''
    :param source_path: like C:\hello
    :param target_path: like C:\myweb\chapter02
    :return: no return
    '''
    if not os.path.exists(target_path):  # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path)
    elif os.path.exists(target_path):  # 如果目标路径存在原文件夹的话就先删除
        # Git has some readonly files. You need to change the permissions first:
        for root, dirs, files in os.walk(target_path):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)

        shutil.rmtree(target_path, ignore_errors=False, onerror=handleRemoveReadonly)

    #  copy 文件夹下的所有文件（包括子目录文件）拷贝到目标文件夹下。 但是这个文件夹本身也被copy 过去。 保持原来的结构
    shutil.copytree(source_path, target_path)

    # copy 文件夹下的所有文件（包括子目录文件）拷贝到目标文件夹下。 但是这个文件夹本身的这个外壳不被copy到目标文件夹。不保持原来的结构
    # root 所指的是当前正在遍历的这个文件夹的本身的地址
    # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
    # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
    # for root, dirs, files in os.walk(source_path):
    #     for file in files:
    #         src_file = os.path.join(root, file)
    #         shutil.copy(src_file, target_path)
    #         print(src_file)

    print('Copy files finished!: ' + source_path + '  to  ' + target_path)


def copyFileToBackupDir():
    # define the command variable which contains path
    source_path_userprofile = r'c:\Users\yzh'
    target_path_root = r'r:\yzh\Backup_App'

    # bash
    target_path_root_bash = os.path.join(target_path_root, 'bash')
    copyFileToFile(os.path.join(source_path_userprofile, '.bash_profile'),
                   os.path.join(target_path_root_bash, '.bash_profile'))
    copyFileToFile(os.path.join(source_path_userprofile, '.bash_history'),
                   os.path.join(target_path_root_bash, '.bash_history'))
    copyFileToFile(os.path.join(source_path_userprofile, '.bashrc'), os.path.join(target_path_root_bash, '.bashrc'))

    # git
    target_path_root_git = os.path.join(target_path_root, 'git')
    copyFileToDir(os.path.join(source_path_userprofile, '.gitconfig'), '.gitconfig', target_path_root_git)
    copyFileToDir(os.path.join(source_path_userprofile, 'git-completion.bash'), 'git-completion.bash',
                  target_path_root_git)

    # .zlua
    copyFileToFile(os.path.join(source_path_userprofile, '.zlua'), os.path.join(target_path_root, '.zlua'))

    ##small app
    # totalcommand
    source_path_root_GHISLER = os.path.join(source_path_userprofile,
                                            r'AppData\Roaming\GHISLER')  # r'c:\Users\yzh\AppData\Roaming\GHISLER'
    target_path_root_TotalCommander = os.path.join(target_path_root,
                                                   r'App_Small\TotalCommander_ConfigDatei')  # 'r:\yzh\Backup\App_Small\TotalCommander_ConfigDatei'
    copyFileToDir(os.path.join(source_path_root_GHISLER, 'usercmd.ini'), 'usercmd.ini', target_path_root_TotalCommander)
    copyFileToDir(os.path.join(source_path_root_GHISLER, 'wcx_ftp.ini'), 'wcx_ftp.ini', target_path_root_TotalCommander)
    copyFileToDir(os.path.join(source_path_root_GHISLER, 'wincmd.ini'), 'wincmd.ini', target_path_root_TotalCommander)

    # other
    source_path_root_ssh = os.path.join(source_path_userprofile, '.ssh')  #
    target_path_root_ssh = os.path.join(target_path_root, 'SSH')  #
    copyDirToDir(source_path_root_ssh, target_path_root_ssh)

    # IDE
    source_path_root_JetBrains = os.path.join(source_path_userprofile, r'AppData\Roaming\JetBrains')  #
    target_path_root_JetBrains = os.path.join(target_path_root, 'App_IDE')  #

    copyDirToDir(os.path.join(source_path_root_JetBrains, 'IdeaIC2022.2'), os.path.join(target_path_root_JetBrains,
                                                                                        'IdeaIC2022.2'))  # r'c:\Users\yzh\AppData\Roaming\JetBrains\IdeaIC2022.2', r'r:\yzh\Backup\App_IDE\IdeaIC2022.2')
    shutil.rmtree(os.path.join(target_path_root_JetBrains, r'IdeaIC2022.2\settingsRepository'), ignore_errors=False,
                  onerror=handleRemoveReadonly)  # r'r:\yzh\Backup_App\App_IDE\IdeaIC2022.2\settingsRepository'

    copyDirToDir(os.path.join(source_path_root_JetBrains, 'PyCharmCE2022.2'),
                 os.path.join(target_path_root_JetBrains,
                              'PyCharmCE2022.2'))  # r'c:\Users\yzh\AppData\Roaming\JetBrains\PyCharmCE2022.2', r'r:\yzh\Backup\App_IDE\PyCharmCE2022.2')
    # shutil.rmtree(os.path.join(target_path_root_JetBrains, r'PyCharmCE2022.2\settingsRepository'), ignore_errors=False, onerror=handleRemoveReadonly)  # r'r:\yzh\Backup_App\App_IDE\IPyCharmCE2022.2\settingsRepository'

    print('Files synchron to Backup Dir finished!')


def handleRemoveReadonly(func, path, exc):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def gitRepoSynchron(target_path: str):
    repo = git.Repo(path=target_path)
    repo.git.add(u=True)
    repo.index.commit('commit at ' + str(strftime(time_format, gmtime())))
    repo.remotes.origin.push()
    repo.remotes.origin.pull()

    print('Git Repo synchron finished!: ' + target_path)

########################################################################################################################
#   MAIN FUNCTION                                                                                                      #
########################################################################################################################
def main():
    # output the log
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"  # '%(asctime)s:%(levelname)s:%(message)s'
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(
        filename=r'r:\yzh\BackupUpdateAndUpload.log',
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        filemode='w'
    )
    logging.info("Backup starts")

    copyFileToBackupDir()

    # git repo synchron
    gitRepoSynchron(r'r:\yzh\Backup_App')


if __name__ == '__main__':
    main()
