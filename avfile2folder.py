import os
import shutil
import datetime
import json
from pprint import pprint
from pymediainfo import MediaInfo
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

source_folder = './'
list_folder = os.listdir(source_folder)
#print(list_folder)


arquivos = []
for path in list_folder:
    # check if current path is a file
    if os.path.isfile(os.path.join(source_folder, path)):
        
        #arquivos.append(path)
        full_path = os.path.join(source_folder, path)
        #print(full_path)

        media_info = MediaInfo.parse(full_path, output="JSON")
        file = json.loads(media_info)["media"]["track"][0]

        fileExtensionFilterVideo = ['MOV', 'MP4']
        fileExtensionFilterPhoto = ['JPG', 'JPEG']
        

        if (file['FileExtension'] in (fileExtensionFilterVideo + fileExtensionFilterPhoto)):

            if (file['FileExtension'] in fileExtensionFilterPhoto):
                im = Image.open(file['CompleteName'])
                exif = dict((ExifTags.TAGS[k], v) for k, v in im._getexif().items() if k in ExifTags.TAGS)
                print('FOTO: ')
                try:
                    anoMesDia = exif['DateTime'].split(' ')[0].replace(':', '-')
                    dataStatus = True
                except:
                    dataStatus = False
                #print(exif)
                #print('========\n\n')

            elif (file['FileExtension'] in fileExtensionFilterVideo): 
                #print('CompleteName: ', file['CompleteName'] )
                try:                
                    encoded_date = file['Encoded_Date']
                    #print(encoded_date)
                    anoMesDia = encoded_date.split(' ')[1]
                    dataStatus = True
                except:
                    dataStatus = False
                    print('Erro encoded Date video')
                #print(anoMesDia)

            if dataStatus == True:
                createFolder = os.path.join(source_folder, anoMesDia)
                src_path = file['CompleteName']
                dst_path = createFolder+'/'+file['FileNameExtension']

                try: 
                    os.mkdir(createFolder)
                    
                except FileExistsError:
                    print('Pasta "', createFolder, '" já existente.')
                print(shutil.move(src_path, dst_path))
            else:
                print('Sem info de data para arquivo: ', file['FileNameExtension'])