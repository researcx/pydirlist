import pydirlist, hashlib, piexif
from pydirlist.models.conversions import human_size
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from flask import send_from_directory

@pydirlist.app.route("/")
def dirview():
    folders = []
    folder = pydirlist.request.args.get('f', '')
    foldersel = ""
    folderpath = ""
    if folder:
        folders = folder.split(";")
        for folder in folders:
            if folder:
                folderpath += pydirlist.os.path.basename(folder) + "/"
                foldersel += pydirlist.os.path.basename(folder) + ";"
        #folderpath = pydirlist.os.path.basename(folder) + "/"
    filefolder = pydirlist.os.getcwd() + "/pydirlist/static/files/" + folderpath
    thumbfolder = pydirlist.os.getcwd() + "/pydirlist/static/.thumbnails/"

    image_types = [".jpg", ".jpeg", ".jpe", ".gif", ".png", ".bmp"]
    audio_types = [".mp3",".ogg",".wav"]
    video_types = [".webm",".mp4",".avi",".mpg",".mpeg"]
    text_types = [".txt",".pdf",".doc"]
    archive_types = [".zip",".rar",".7z",".tar",".gz"]

    fileurl = pydirlist.request.url_root + "static/files/" + folderpath
    thumburl = pydirlist.request.url_root + "static/.thumbnails/"
    file_list = []
    image_list = []
    folder_list = []
    for fn in pydirlist.os.listdir(filefolder):
        is_goto = False
        filepath = filefolder + "/" + fn
        if pydirlist.os.path.isdir(filepath):
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            if "_goto_" in fn:
                is_goto = True
                fn = fn.replace('_goto_', '')
            folder_list.append([filetime, fn, is_goto])
        if pydirlist.os.path.isfile(filepath):
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            filesize = pydirlist.os.path.getsize(filepath)
            extension = pydirlist.os.path.splitext(fn)[1].lower()
            hashname = hashlib.sha256(fn.encode()).hexdigest()
            if extension in image_types:
                thumbpath = thumbfolder + hashname + ".png"
                if not pydirlist.os.path.isfile(thumbpath):
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

    return pydirlist.render_template('dir.html', foldercount=len(folder_list), filecount=len(file_list), imagecount=len(image_list), fileurl=fileurl, thumburl=thumburl, folder_list=folder_list, file_list=file_list, image_list=image_list, folderpath=folderpath, foldersel=foldersel, folders=folders)

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
