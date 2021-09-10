import pydirlist, hashlib, piexif
from pydirlist.models.conversions import human_size
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from flask import send_from_directory

@pydirlist.app.route("/xml")
def xmlview():
    folders = []
    folder = pydirlist.request.args.get('f', '')
    foldersel = ""
    folderpath = ""
    breadcrumbs = ""
    is_active = ''
    full_path = ""
    hidden_folders = [".", "NSFW", "Avatars", "Lewd"]
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
    tmp_types = [".tmp"]

    fileurl = pydirlist.request.url_root + "static/files/" + folderpath
    thumburl = pydirlist.request.url_root + "static/.thumbnails/"
    file_list = []
    image_list = []
    folder_list = []
    for fn in pydirlist.os.listdir(filefolder):
        filepath = filefolder + "/" + fn
        if (pydirlist.request.args.get('folders', '') != "") and (pydirlist.os.path.isdir(filepath) and fn[:1] is not "."):
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            is_goto = False
            filepath = filefolder + "/" + fn
            if pydirlist.os.path.isdir(filepath):
                filetime = int(pydirlist.os.stat(filepath).st_mtime)
                if "_goto_" in fn:
                    is_goto = True
                    fn = fn.replace('_goto_', '')
                if fn not in hidden_folders:
                    folder_list.append([filetime, fn, is_goto])
        if (pydirlist.request.args.get('files', '') != "") and (pydirlist.os.path.isfile(filepath) and fn[-1] is not "~"):
            filetime = int(pydirlist.os.stat(filepath).st_mtime)
            filesize = pydirlist.os.path.getsize(filepath)
            extension = pydirlist.os.path.splitext(fn)[1].lower()
            hashname = hashlib.sha256(fn.encode()).hexdigest()

            if extension in link_types:
                url = ""
                with open(filefolder + fn) as f:
                    url = f.readlines()
                type_icon = '<i class="fa fa-arrow-circle-right file-icon" aria-hidden="true"></i>'
                file_list.append([filetime, filesize, fn.split(".")[0], type_icon, url[0]])
                f.close()
            else:
                if extension not in link_types:
                     if extension not in tmp_types:
                         type_icon = '<i class="fa fa-file-o file-icon" aria-hidden="true"></i>'
                         file_list.append([filetime, filesize, fn, type_icon, ""])

    count = int(pydirlist.request.args.get('count', ''))

    list_combined = []
    list_combined.extend(file_list)
    list_combined.extend(folder_list)

    file_list.sort(reverse=True)
    folder_list.sort(reverse=True)
    list_combined.sort(reverse=True)

    file_list = file_list[:count]
    folder_list = folder_list[:count]
    latest_file = list_combined[0:1]

    return pydirlist.render_template('xml.html', latest_file=latest_file[0], foldercount=len(folder_list), filecount=len(file_list), fileurl=fileurl, thumburl=thumburl, folder_list=folder_list, file_list=file_list, folderpath=folderpath, foldersel=foldersel, breadcrumbs=breadcrumbs, folders=folders)
