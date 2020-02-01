#
# Copyright (c) 2020 by unendingPattern (https://unendingpattern.github.io). All Rights Reserved.
# You may use, distribute and modify this code under WTFPL.
# The full license is included in LICENSE.md, which is distributed as part of this project.
#

import keiDirList, hashlib, piexif
from keiDirList.models.conversions import human_size
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from flask import send_from_directory

@keiDirList.app.route("/")
def dirview():
    folders = []
    folder = keiDirList.request.args.get('f', '')
    foldersel = ""
    folderpath = ""
    if folder:
        folders = folder.split(";")
        for folder in folders:
            if folder:
                folderpath += keiDirList.os.path.basename(folder) + "/"
                foldersel += keiDirList.os.path.basename(folder) + ";"
        #folderpath = keiDirList.os.path.basename(folder) + "/"
    filefolder = keiDirList.os.getcwd() + "/keiDirList/static/files/" + folderpath
    thumbfolder = keiDirList.os.getcwd() + "/keiDirList/static/.thumbnails/"

    image_types = [".jpg", ".jpeg", ".jpe", ".gif", ".png", ".bmp"]
    audio_types = [".mp3",".ogg",".wav"]
    video_types = [".webm",".mp4",".avi",".mpg",".mpeg"]
    text_types = [".txt",".pdf",".doc"]
    archive_types = [".zip",".rar",".7z",".tar",".gz"]

    fileurl = keiDirList.request.url_root + "static/files/" + folderpath
    thumburl = keiDirList.request.url_root + "static/.thumbnails/"
    file_list = []
    image_list = []
    folder_list = []
    for fn in keiDirList.os.listdir(filefolder):
        filepath = filefolder + "/" + fn
        if keiDirList.os.path.isdir(filepath):
            filetime = int(keiDirList.os.stat(filepath).st_mtime)
            folder_list.append([filetime, fn])
        if keiDirList.os.path.isfile(filepath):
            filetime = int(keiDirList.os.stat(filepath).st_mtime)
            filesize = keiDirList.os.path.getsize(filepath)
            extension = keiDirList.os.path.splitext(fn)[1].lower()
            hashname = hashlib.sha256(fn.encode()).hexdigest()
            if extension in image_types:
                thumbpath = thumbfolder + hashname + ".png"
                if not keiDirList.os.path.isfile(thumbpath):
                    im = Image.open(filepath)
                    im = ImageOps.fit(im, (160, 100),  Image.ANTIALIAS)
                    im.save(thumbpath, "PNG")
                image_list.append([filetime, filesize, fn, hashname])
            elif extension in audio_types:
                type_icon = '<i class="fa fa-file-audio-o" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon])
            elif extension in video_types:
                type_icon = '<i class="fa fa-file-video-o" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon])
            elif extension in text_types:
                type_icon = '<i class="fa fa-file-text-o" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon])
            elif extension in archive_types:
                type_icon = '<i class="fa fa-file-archive-o" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon])
            else:
                type_icon = '<i class="fa fa-file-o" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon])

    file_list.sort(reverse=True)

    return keiDirList.render_template('dir.html', foldercount=len(folder_list), filecount=len(file_list), imagecount=len(image_list), fileurl=fileurl, thumburl=thumburl, folder_list=folder_list, file_list=file_list, image_list=image_list, folderpath=folderpath, foldersel=foldersel, folders=folders)

## Redirect /pics/ to /?f=pics;
# @keiDirList.app.route("/pics/")
# def pics_redirect():
# 	return keiDirList.redirect("/?f=pics;", code=301)
 
@keiDirList.app.route('/robots.txt')
def robotstxt():
    return send_from_directory(keiDirList.app.static_folder, keiDirList.request.path[1:])

@keiDirList.app.route('/humans.txt')
def humanstxt():
    return send_from_directory(keiDirList.app.static_folder, keiDirList.request.path[1:])

@keiDirList.app.route('/favicon.ico')
def faviconico():
    return send_from_directory(keiDirList.app.static_folder, keiDirList.request.path[1:])
