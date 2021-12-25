import PIL
from django.shortcuts import render,redirect

from main_app.models import *

import os
from PIL import Image
# Create your views here.

def index(request):
    if request.method=='POST':
        user_photo=request.FILES['user_photo']
        print(user_photo)

        if image_handler.objects.filter(user_image=user_photo).exists():

            return render(request,'index.html',{'checker':'Error.. Please refresh the window'})
        else:
            temp_img=image_handler() #custom db object
            temp_img.user_image=user_photo
            temp_img.save()
            print('image saved')

            media_contents=os.listdir('media/') # colleecting media folder all images and pass to the function add_watermark()
            print(media_contents)
            for my_img in media_contents:
                print(my_img,'my_img')

            # main image compress condition code
            # img=Image.open('media/group.JPG')
            img=Image.open('media/'+ my_img)
            # img=os.listdir('media/group.JPG')
            width ,height = img.size
            img=img.resize((width,height),PIL.Image.ANTIALIAS)
            img.save('media/compressed/' + 'compressed.jpg')

            return redirect(viewer)

    

    # main case //////////////////////////////////////////////////
    # deleteing temporary data fom image_handler db
    myimagedb=image_handler.objects.all() # callimg all image_handler db for deleting
    print(myimagedb.count(),'the count')

    if myimagedb.count() > 0: # database checker

        #1 delete all user temporary value image from main media folder
        for image_remover in myimagedb: # this is for passing queryset value
            # print(myimagedb.count(),'the for loop count')

            if len(image_remover.user_image) > 0: # it will check the old image is not empty or not
                os.remove(image_remover.user_image.path)  #then delete the image

        print('main media folder deleted')

        #2 delete all user temporary database image
        myimagedb.delete()
        print('all user temporary database deleted') 

    # # delete all user temporary converted image from converted folder(media/converted/media)
    compressed=os.listdir('media/compressed/') #delete converted image
    for deleteimg in compressed:
        print(deleteimg,'deleteimg')
        os.remove('media/compressed/'+deleteimg)
        
    print('all compressed images deleted ')

    # main case //////////////////////////////////////////////////

    return render(request,'index.html',{})


def viewer(request):

    myimagedb=image_handler.objects.all()
    for content in myimagedb:
        print(content,'content') 
    # counter=myimage.count()
    # print(counter)
    # for x in myimage:
    #     print(x.user_image)

    if myimagedb.count() == 0 :
        print('if')
        return redirect(index)
    
    else:
        print('else')

        converded=os.listdir('media/compressed/')
        for converted_imagename in converded:
            print(converted_imagename,'converted_imagename')


        # image size calculator
        src = 'media/compressed/'+converted_imagename
        abc=os.path.getsize(src)
        print(abc,'uytuyt')
        result=(abc/1024/1024)

        float = result
        format_float = "{:.2f}".format(float)
        print(format_float,'MB')

        return render(request,'viewer.html',{'imagesize':format_float,'imagename':converted_imagename})
    





    # src = 'img1.jpg'
    # abc=os.path.getsize(src)
    # image = Image.open(src)
    # sizeabc =  image.size
    # print(sizeabc)
    # print(abc)
