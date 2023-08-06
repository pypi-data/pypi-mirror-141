import pandas as pd
import subprocess as _subprocess

def _conda_list_subprocess():
    
    """"""
    
    return _subprocess.run(['conda', 'list'], stdout=_subprocess.PIPE, stderr=False).stdout.decode()

def _get_conda_list_df(conda_list):
    
    """"""
    
    LinuxDict = {}
    EnvDict = {}
    LinuxDict_LineCount = 0
    EnvDict_LineCount = 0
    for line in conda_list.split('\n'):
        newline = []
        for word in line.split(' '):
            if len(word) >  1:
                newline.append(word)
        if len(newline) == 3:
            LinuxDict[LinuxDict_LineCount] = newline
            LinuxDict_LineCount += 1
        elif len(newline) == 4:
            EnvDict[EnvDict_LineCount] = newline
            EnvDict_LineCount += 1

    env_df = pd.DataFrame.from_dict(EnvDict).T
    env_df.columns = env_df.iloc[0]
    env_df = env_df[1:]

    linux_df = pd.DataFrame.from_dict(LinuxDict).T
    env_df_cols = env_df.columns.to_list()
    linux_df.columns = env_df_cols[:3]
    linux_df[env_df_cols[-1]] = "None"
    conda_list_df = pd.concat([linux_df, env_df])
    return conda_list_df

def _get_mscorefonts():
    
    """"""
    
    conda_list = _conda_list_subprocess()
    conda_list_df = _get_conda_list_df(conda_list)
    if not 'mscorefonts' in conda_list_df['Name'].to_list():
        download_log = _subprocess.run(['conda', 'install', '-c', 'conda-forge', 'mscorefonts', '-y'], stdout=_subprocess.PIPE, stderr=False)
        return download_log
    else:
        return "installed"
