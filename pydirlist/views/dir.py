import pydirlist, hashlib, piexif, os
from pydirlist.models.conversions import human_size
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from flask import send_from_directory
from multiprocessing import Pool

def do_thumbnail(filepath):
    snapshotCommand = "/bin/sh /root/pydirlist/thumbnailer.sh \"" + filepath + "\""  
    os.system(snapshotCommand)                                              

@pydirlist.app.route("/")
def dirview():
    folders = []
    folder = pydirlist.request.args.get('f', '')
    foldersel = ""
    folderpath = ""
    is_gallery = True if pydirlist.request.args.get('gallery', '') != "" else False
    show_all = True if pydirlist.request.args.get('all', '') != "" else False
    breadcrumbs = ""
    is_active = ''
    full_path = ""
    hidden_folders = [".", "NSFW"]
    if folder and folder[:1] is not ".":
        folders = folder.split(";")
        while("" in folders): 
            folders.remove("")
        for folder in folders:
            if folder and folder[:1] is not ".":
                folderpath += pydirlist.os.path.basename(folder) + "/"
                foldersel += pydirlist.os.path.basename(folder) + ";"
            full_path += folder + ";" 
            if folder == folders[-1]:
                is_active = ' class="active"' 
            breadcrumbs += '<li'+is_active+'><a href="/?f='+full_path+'">'+folder+'</a></li>'
                
        #folderpath = pydirlist.os.path.basename(folder) + "/"
    filefolder = pydirlist.os.getcwd() + "/pydirlist/static/files/" + folderpath
    thumbfolder = pydirlist.os.getcwd() + "/pydirlist/static/.thumbnails/"

    image_types = [".jpg", ".jpeg", ".jpe", ".gif", ".png", ".bmp"]
    audio_types = [".mp3",".ogg",".wav"]
    video_types = [".webm",".mp4",".avi",".mpg",".mpeg"]
    text_types = [".txt",".pdf",".doc"]
    archive_types = [".zip",".rar",".7z",".tar",".gz"]
    link_types = [".link", ".url", ".goto", ".shortcut"]

    fileurl = pydirlist.request.url_root + "static/files/" + folderpath
    thumburl = pydirlist.request.url_root + "static/.thumbnails/"
    file_list = []
    image_list = []
    folder_list = []
    files = []
    for fn in pydirlist.os.listdir(filefolder):
        filepath = filefolder + "/" + fn
        if pydirlist.os.path.isdir(filepath) and fn[:1] is not ".":
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            is_goto = False
            filepath = filefolder + "/" + fn
            if pydirlist.os.path.isdir(filepath):
                filetime = int(pydirlist.os.stat(filepath).st_mtime)
                if "_goto_" in fn:
                    is_goto = True
                    fn = fn.replace('_goto_', '')
                if show_all:
                    folder_list.append([filetime, fn, is_goto])
                elif fn not in hidden_folders:
                    folder_list.append([filetime, fn, is_goto])
        if pydirlist.os.path.isfile(filepath) and fn[-1] is not "~":
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            filesize = pydirlist.os.path.getsize(filepath)
            extension = pydirlist.os.path.splitext(fn)[1].lower()
            hashname = hashlib.sha256(filepath.encode()).hexdigest()

            if extension in link_types:
                url = ""
                with open(filefolder + fn) as f:
                    url = f.readlines()
                type_icon = '<i class="fa fa-arrow-circle-right file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn.split(".")[0], type_icon, url[0]])
                f.close()

            if extension in image_types:
                thumbpaths = [thumbfolder + hashname + "-150.jpg"]
                if extension == ".gif":
                   image_list.append([filetime, filesize, fn, '/static/files/'+foldersel.strip(";")+'/' + fn + '?v='])
                else:
                    for thumbpath in thumbpaths:
                        if not pydirlist.os.path.isfile(thumbpath):
                            do_thumbnail(filepath)
                    image_list.append([filetime, filesize, fn, '/static/.thumbnails/' + hashname])
            elif extension in audio_types:
                type_icon = '<i class="fa fa-file-audio-o file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon, ""])
            elif extension in video_types:
                type_icon = '<i class="fa fa-file-video-o file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon, ""])
            elif extension in text_types:
                type_icon = '<i class="fa fa-file-text-o file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon, ""])
            elif extension in archive_types:
                type_icon = '<i class="fa fa-file-archive-o file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn, type_icon, ""])
            else:
                if extension not in link_types:
                  type_icon = '<i class="fa fa-file-o file-icon" aria-hidden="true"></i>'
                  file_list.append([filetime, filesize, fn, type_icon, ""])
                  
    file_list.sort(reverse=True)
    image_list.sort(reverse=True)
    folder_list.sort(reverse=True)

    return pydirlist.render_template('dir.html', foldercount=len(folder_list), filecount=len(file_list), imagecount=len(image_list), fileurl=fileurl, thumburl=thumburl, folder_list=folder_list, file_list=file_list, image_list=image_list, folderpath=folderpath, foldersel=foldersel, breadcrumbs=breadcrumbs, folders=folders, is_gallery=is_gallery)

## Redirect /pics/ to /?f=pics;
# @pydirlist.app.route("/pics/")
# def pics_redirect():
# 	return pydirlist.redirect("/?f=pics;", code=301)
 
@pydirlist.app.route('/robots.txt')
def robotstxt():
    return send_from_directory(pydirlist.app.static_folder, pydirlist.request.path[1:])

@pydirlist.app.route('/humans.txt')
def humanstxt():
    return send_from_directory(pydirlist.app.static_folder, pydirlist.request.path[1:])

@pydirlist.app.route('/favicon.ico')
def faviconico():
    return send_from_directory(pydirlist.app.static_folder, pydirlist.request.path[1:])
