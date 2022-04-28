import os
import json
import sys

from PIL import Image

image_types = ['.jpg', '.png', '.jpeg', '.bmp', '.gif']
bg_color = (0, 0, 0)

def buildImage(file_path, new_path, to_width, to_height):
    
    img = Image.open(file_path)
    width, height = img.size
    if width * to_height > height * to_width:
        height = round((height * to_width) / width)
        width = to_width
    else:
        width = round((width * to_height) / height)
        height = to_height
        
    img = img.resize((width, height))
    img = img.convert('1')
    
    new_img = Image.new('RGB',(to_width, to_height), bg_color)
    s = (round((to_width - width) / 2), round((to_height- height) / 2))
    new_img.paste(img, s)
    new_img.monochrome = True
    new_img.save(new_path)


def buildAllImages(root_path, data_path, to_width, to_height):
    root_path = os.path.abspath(root_path)
    
    files = []
    for (dirpath, dirnames, filenames) in os.walk(root_path):
        for f in filenames:
            filename, ext = os.path.splitext(f)
            if ext in image_types:
                file_path = os.path.join(dirpath, f)
                file_path = os.path.abspath(file_path)
                files.append(file_path)
    
    keys = {}
    keys_path = data_path + 'keys.json'
    if os.path.isfile(keys_path):
        f = open(keys_path)
        try:            
            js = json.load(f)
            for key in js:
                keys[key] = js[key]
        except e:
            print(e)
        #data = json.load(f)
    
    force = "force" in sys.argv
    has_change = force
    
    for f in files:
        key = f + '_' + str(os.path.getsize(f)) + '_' + str(os.path.getctime(f))
        
        head, tail = os.path.split(f)
        
        new_path = data_path + '/images/' + tail + '.bmp'
        
        if not force and key in keys and keys[key] == new_path and os.path.isfile(new_path):
            continue
            
        keys[key] = new_path
        
        has_change = True
        buildImage(f, new_path, to_width, to_height)
        print('added ' + new_path)
        
    if has_change:
        f = open(keys_path, 'w')
        json.dump(keys, f)
        

def main():
    root_path = './test_images/'
    data_path = './data/'
    
    to_width = 400
    to_height = 300
    
    buildAllImages(root_path, data_path, to_width, to_height)
    
if __name__ == '__main__':
    main()

