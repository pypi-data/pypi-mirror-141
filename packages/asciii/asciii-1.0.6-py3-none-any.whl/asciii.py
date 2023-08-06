from PIL import Image
import os,sys

####################################

class asciii():
    
    cols_patterns=[
        "",
        '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`". ',
        "@%#*+=-:. "
    ]
    im_map=""

    def __init__(self,pattern=0,max_size=0,shift=0):
        if isinstance(pattern,str):
            self.cols=pattern
        else:
            self.cols=self.cols_patterns[int(pattern)]
        if max_size!=0:
            self.maxs(max_size)
        else:
            self.maxs()
        self.shift=shift
    
    def maxs(self,size=140):
        self.max_size=(size,size)

    def remap(self,OldValue,OldMin,OldMax,NewMin,NewMax,roundnum=True):
        OldRange = (OldMax - OldMin)  
        NewRange = (NewMax - NewMin)  
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        if roundnum:
            NewValue=round(NewValue)
        return NewValue

    def cls(self):
        os.system("cls")

    def colored(self,r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def product(self,file):
        if isinstance(file,str):
            self.file_name=file
            self.cls()
            im = Image.open(self.file_name)
        else:
            im = Image.fromarray(file)
        im.thumbnail(self.max_size, Image.ANTIALIAS)
        #im.save("2.jpg")
        width, height = im.size
        rgb_im = im.convert('RGB')
        for y in range(height):
            if y%2==1:
                for x in range(width):
                    r, g, b = rgb_im.getpixel((x, y))
                    s=min(((r+g+b)/3)+self.shift,255)
                    s=self.remap(s,0,255,0,len(self.cols)-1)
                    #self.im_map+=self.colored(r,g,b,self.cols[s])
                    if self.cols=="":
                        self.im_map+=f"\033[48;2;{r};{g};{b}m{''} \033[0m"
                    else:
                        self.im_map+=self.cols[s]
                self.im_map+="\n"
                #self.im_map=""
        imap=self.im_map
        self.im_map=""
        return imap

if __name__=="__main__":
    args=sys.argv
    args.append(0)
    args.append(0)
    print(asciii(args[2],int(args[3]),int(args[4])).product(args[1]))
####py ita.py filename pattern size