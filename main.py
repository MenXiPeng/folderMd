import os, shutil, fnmatch
import re
from enum import Enum
path = "/Users/menxipeng/logs/电视剧"

#path = input("请输入跟路径：")


def is_root_folder(rootpath, pre_path):
    paths = os.listdir(rootpath)
    # 保留上一个文件夹的名称
    currentDir = pre_path
    for file in paths:
        file_path = os.path.join(rootpath, file)
        # 不包含网址不去修改
        if not contains_site(file):
            print("不包含网址直接跳过", file)
            continue
        # 文件夹处理
        if os.path.isdir(file_path):
            currentDir = file_path
            print("it's a directory ", file)
            newName = match_folder(file)
            newPath = os.path.join(rootpath, newName)
            if not os.path.exists(newPath):
                tempPath = file_path
                os.rename(tempPath, newPath)
                is_root_folder(newPath, currentDir)
            else:
                is_root_folder(file_path, currentDir)
        # 文件处理
        if os.path.isfile(file_path) and contains_file(file_path):
            if not (file.startswith('.') and os.path.isfile(file_path)):
                if contains_site(file_path):
                    print("删除包含网址的广告文件：", file_path)
                    os.remove(file_path)
                else:
                    file_handler(file_path, currentDir)
                continue
        else:
            # 删除不是 mkv 的文件
            if os.path.exists(file_path):
                print("删除非 mkv 文件：", file_path)
                os.remove(file_path)
        newName = match_folder(file)
        newPath = os.path.join(rootpath, newName)
        if os.path.exists(newPath) and os.path.exists(currentDir):
            season = match_season(file)
            sFolderName = get_season(season)
            pf = os.path.join(rootpath, file)
            oldPath = os.path.join(pf, sFolderName)
            print("开始移动到相同文件目录下:", oldPath)
            shutil.move(oldPath, newPath)
            shutil.rmtree(os.path.join(rootpath, file))


def file_handler(file_path, current_dir):
    # 匹配上一个文件夹的名称用于获取第几季
    seasonFolder = None
    season = match_season(current_dir)
    s_folder_mame = get_season(season)
    print("获取到季的文件夹名称：", s_folder_mame)
    if s_folder_mame is not None:
        filepath, fullname = os.path.split(file_path)
        seasonFolder = os.path.join(filepath, s_folder_mame)
        # 创建季数的文件夹
        print("创建季文件夹：", seasonFolder)
        if not os.path.exists(seasonFolder):
            os.makedirs(seasonFolder)
        seasonPath = os.path.join(seasonFolder, fullname)
        if not match_file_name(fullname, (season + "E")):
            # 处理文件名称
            newName = modify_file_name(fullname, season)
            seasonPath = os.path.join(seasonFolder, newName)
            print("修改文件名：", newName)
            print("开始移动修改文件名后：", file_path, " to ", seasonPath)
            shutil.move(file_path, seasonPath)
        else:
            print("开始移动：", file_path, " to ", seasonPath)
            shutil.move(file_path, seasonPath)
        return seasonFolder
    # if existPath != "" and seasonFolder is not None:
    #     # 移动到原先的路径下，删除原路径
    #     shutil.move(seasonFolder, existPath)


class SeasonEnum(Enum):
    S01 = "Season 1"
    S02 = "Season 02"
    S03 = "Season 03"
    S04 = "Season 04"
    S05 = "Season 05"
    S06 = "Season 06"
    S07 = "Season 07"
    S08 = "Season 08"
    S09 = "Season 09"
    S10 = "Season 10"
    S11 = "Season 11"
    S12 = "Season 12"


def get_season(season):
    for k, _ in SeasonEnum.__members__.items():
        if season == k:
            return SeasonEnum[k].value


def match_season(dir_name):
    seasonObj = re.search('S[0-9]{1,}', dir_name)
    if seasonObj:
        return seasonObj.group()
    else:
        return "S01"


def match_folder(dir_name):
    return dir_name.split("】")[1].split("[")[0]


def match_file_name(file_name, season):
    findNameCount = file_name.count(season)
    return findNameCount > 0


def modify_file_name(filename, season):
    ep = re.search("E[0-9]{1,}", filename, re.M)
    if ep:
        sep = season + ep.group()
        newName = filename.replace(ep.group(), sep)
        return newName


def contains_site(file):
    # [a-zA-Z]{1,3}
    site = re.search("(www)(\\.){1}[a-zA-Z]{1,}(\\.){1}[a-zA-Z]{1,3}", file, re.M)
    return site is not None


def contains_file(file):
    return fnmatch.fnmatch(file,"*.mkv")


# def match_file_name(fileName):
#     fileName.con


# 【高清剧集网 www.BTHDTV.com】睡魔[全10集][简繁英字幕].The.Sandman.2022.S02.V2.1080p.NF.WEB-DL.H264.DDP5.1.Atmos-Meizu
# print(season_enum.S01.value)

# match_folder("【高清剧集网 www.BTHDTV.com】睡魔[全10集][简繁英字幕].The.Sandman.2022.S01.V2.1080p.NF.WEB-DL.H264.DDP5.1.Atmos-Meizu")
is_root_folder(path, "")

#print(contains_file("ss/ddd/1111.mkv"))
# modify_file_name("Season 1The.Sandman.2022.S01E01.V2.1080p.NF.WEB-DL.H264.DDP5.1.Atmos-Meizu 2", "S01")
# print("sss"+"/aa")
