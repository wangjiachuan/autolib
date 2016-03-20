#! /usr/bin/env python
#-*- coding: utf8 -*-
'This is the template for the test case, test case inherit this '
'2016-03-02'
import os
import sys
import time
import unittest
import virtkey
import logging
import commands
import re
import Xlib.display as ds
import Xlib.X as X
import Xlib.ext.xtest as xtest
import gtk.gdk


class TestCaseFramework(unittest.TestCase):


    def setUp(self):
        print ('setUp...')
        self.v = virtkey.virtkey()
        self.username = os.getlogin()
        self.filename = 'abcd'
        self.clean_screenshot()
        
    def tearDown(self):
        print ('tearDown...')                           
        self.quit_cmd()

    def quit_cmd(self):
        '''
        quit the cmd input box, should be called in teardown()
        '''
        time.sleep(0.5)
        self.v.press_keysym(65307)#Esc
        self.v.release_keysym(65307)
        #ctr+w
        time.sleep(0.5)
        self.v.press_keysym(65507)#Ctr
        time.sleep(0.5)
        self.v.press_unicode(ord('w'))# w
        time.sleep(0.5)
        self.v.release_unicode(ord('w'))
        time.sleep(0.5)
        self.v.release_keysym(65507)
        #ctr+q
        time.sleep(0.5)
        self.v.press_keysym(65507)#Ctr
        time.sleep(0.5)
        self.v.press_unicode(ord('q'))# w
        time.sleep(0.5)
        self.v.release_unicode(ord('q'))
        time.sleep(0.5)
        self.v.release_keysym(65507)


    def open_app(self,app_name):
        #self.open_app_by_command(app_name)
        self.open_app_by_gui(app_name)

    def open_app_by_gui(self,app_name):
        self.mouse_click(1,39,1056)
        self.mouse_click(1,172,472)
        self.keyboard_input(app_name)
        #enter
        time.sleep(0.5)
        self.v.press_keysym(65421)#enter
        time.sleep(0.5)
        self.v.release_keysym(65421)
        time.sleep(3)
        
        
    def open_app_by_command(self,app_name):
        '''
        open the application 
        '''
        #Alt+f2
        self.v.press_keysym(65513)#Alt 
        self.v.press_keysym(65471)#f2
        self.v.release_keysym(65471)
        self.v.release_keysym(65513)

        # input app name
        keyboard_list = list(app_name)
        for i in keyboard_list:
            time.sleep(0.2)
            self.v.press_unicode(ord(i))
            time.sleep(0.2)
            self.v.release_unicode(ord(i))

        #enter
        time.sleep(0.5)
        self.v.press_keysym(65421)#enter
        time.sleep(0.5)
        self.v.release_keysym(65421)
        time.sleep(3)
        
        
    def save_file(self,filename):
        '''
        save the file(ctr+s),input the file name,quit the application (ctr+q)
        
        '''
        print ('step 3) save the file and close file')
        time.sleep(0.5)
        self.v.press_keysym(65507)#Ctr
        time.sleep(0.5)
        self.v.press_unicode(ord('s'))# s
        time.sleep(0.5)
        self.v.release_unicode(ord('s'))
        time.sleep(0.5)
        self.v.release_keysym(65507)

        #file name is abc
        self.keyboard_input(filename)

        #input enter to save
        time.sleep(0.5)
        self.v.press_keysym(65421)#enter
        self.v.release_keysym(65421)

        #ctr+q to quit gedit
        time.sleep(0.5)
        self.v.press_keysym(65507)#Ctr
        time.sleep(0.5)
        self.v.press_unicode(ord('q'))# q
        time.sleep(0.5)
        self.v.release_unicode(ord('q'))
        time.sleep(0.5)
        self.v.release_keysym(65507)
        

    def keyboard_input(self,keyboard_string):
        '''
        simulate keyboard stroke, input the string
        ''' 
        time.sleep(2)        
        keyboard_list = list(keyboard_string)
        for i in keyboard_list:
            time.sleep(0.2)
            self.v.press_unicode(ord(i))
            time.sleep(0.2)
            self.v.release_unicode(ord(i))
            

    def check_file_content_exist(self,path,filename,content):
        '''
        check the file exist, and the content is right. 
        '''        
        if os.path.exists(path+r'/'+filename):
            with open(str(path+r'/'+filename),"r") as f:
                f.seek(0,0)
                lines = f.readlines()
                for line in lines:
                    print ("content in file is %s".format(line))
                    if(line.find(content)==-1):
                        continue
                    else:
                        print ("find the content!")
                        return True  
        else:             
            return False
        

    def check_file_exist(self,path,filename):
        '''
        check the file exist. 
        '''
        print ('step 2) check the file %s exist in %s'%(filename,path))
        return os.path.exists(path+r'/'+filename)
    

    def check_dir_not_empty(self,rootdir):
        '''
        check the directory is not empty
        '''
        for root,dirs,files in os.walk(self.rootdir):
            if(len(files)== 0):
                print("not find any files")
                return False
            else:
                print("find files")
                return True

    def check_process_exist(self,processname):
        '''
        check the app process exist. 
        '''
    
        for line in os.popen("ps xa"):
            fields = line.split()
            pid = fields[0]
            process = fields[4]

            if process.find(processname)==0:
                print("A: does find %s!!"%processname)
                return True
            else:
                #print("A:does not find it!!")
                pass

        return False
    

    def check_app_windows_exist(self,appname):
        '''
        check the app windows exist. 
        '''
        #get screen shot
        self.screen_shot(appname+".jpeg")
        print ('check the app %s exist'%appname)
        return self.check_process_exist(appname)
    
    

    def remove_all_files(self,directory):
        '''
        remove all the files in the directory
        '''
        filelist = []        
        filelist = os.listdir(directory)
        for f in filelist:
            filepath = os.path.join(directory,f)
            if os.path.isfile(filepath):
                os.remove(filepath)
                

    def remove_file(self,directory,filename):
        '''
        remove specific file in the directory
        '''
        if os.path.exists(directory+os.sep+filename):
            os.remove(directory+os.sep+filename)

    def clean_screenshot(self):
        self.remove_file(os.getcwd(),self.get_case_name()+'.html')
        
        # list all the existing screenshot for this test case
        files = os.listdir(os.getcwd())
        case_name = self.get_case_name()
        
        # get the latest picture
        jpeg_list = [x for x in files if (case_name in x) and x.lower().endswith('.jpeg')]

        for item in jpeg_list:
            print("delete screenshot: %s" % item)
            self.remove_file(os.getcwd(),item)


    def command_check(self,command_line,expection):

        "execute a command, check if the expection value is in the output of the command line"
        
        print("current working dir is : %s" % (os.getcwd()))
        os.chdir(os.getcwd())     
        
        print("command is: %s" % (command_line))
        feedback = commands.getstatusoutput(command_line)
        print("command output is:")
        print(feedback)

        prog = re.compile(expection)
        result = prog.findall(feedback[1])
        print("search result is:")
        print(result)
        
        if expection in result:
            print("find it")
            return True
        else:
            print("does not find it")
            return False



    def mouse_click(self,button,x,y):
        '''
        move the mouse to (x,y), click mouse button.
        buttton: 1,left, 2,middle,3 right,4 middle up,5 middle down
        '''

        self.display = ds.Display()
        
        xtest.fake_input(self.display,X.MotionNotify,x=x,y=y)
        self.display.flush()
        time.sleep(0.2)

        coord = self.display.screen().root.query_pointer()._data
        print("mouse at:\t\t %d,%d" % (coord["root_x"],coord["root_y"]))

        width=self.display.screen().width_in_pixels
        height = self.display.screen().height_in_pixels
        print("screen is:\t\t %d,%d" % (width,height))
        
        xtest.fake_input(self.display,X.ButtonPress,button)
        self.display.sync()
        time.sleep(1)
        xtest.fake_input(self.display,X.ButtonRelease,button)
        self.display.sync()
        time.sleep(1)


    def mouse_location(self):
        display = ds.Display()
        coord = display.screen().root.query_pointer()._data
        print("mouse at:\t\t %d,%d" % (coord["root_x"],coord["root_y"]))


    def get_case_name(self):      
        return "gedit"

    '''
    def _get_index(self,screeshot_list):
        'find out the max index in the list'
        maxindex = 0
        for item in screeshot_list:
            tmp1 = len(self.get_case_name())-len(item)
            tmp2 = "".join(reversed(list(item)[-1:tmp1-1:-1]))
            print("later part is %s" % tmp2)
            
            index = int("".join(list(tmp2)[:len(tmp2)-5]))
            print("item index is %s" % index)
            if maxindex >= index:
                pass
            else:
                maxindex = index
        print("max index is %d" % maxindex)
        return maxindex
    '''


    def _get_index(self,screeshot_list):
        'find out the max index in the list'
        maxindex = 0
        for item in screeshot_list:
            get_index=re.search(r"(?P<index>\d+).jpeg",item)
            index=int(get_index.group("index"))
            print("item index is %d" % index)
            if maxindex >= index:
                pass
            else:
                maxindex = index
        print("max index is %d" % maxindex)
        return maxindex
     

    def get_pic_name(self):
        files = os.listdir(os.getcwd())
        case_name = self.get_case_name()

        # get the latest picture
        jpeg_list = [x for x in files if (self.get_case_name() in x) and x.lower().endswith('.jpeg')]
        
        if len(jpeg_list) == 0:
            print("create first screen shot")
            target = case_name+str(1)+".jpeg"
        else:
            target = case_name+str(self._get_index(jpeg_list)+1)+".jpeg"

        print("target screenshot name is %s" % target)
        return target


    def screen_shot(self,comment = "",save_dir=os.getcwd()):
        'save the screen shot to a html file.'
        
        pic_name = self.get_pic_name()
        #get screen shot
        windows = gtk.gdk.get_default_root_window()
        size = windows.get_size()
        #print("the size of the window is %d x %d " % (size))
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,size[0],size[1])
        pb = pb.get_from_drawable(windows,windows.get_colormap(),0,0,0,0,size[0],size[1])
        print("save screen as:%s" %(pic_name))
        pb.save(pic_name,'jpeg')

        #save to html
        self.save_to_html(pic_name,comment)

        pass



    def save_to_html(self,picture,comment):
        'add screen shot to html file, add comment to html'

        html = open(self.get_case_name()+'.html','a')
        html.write("""
        <html>
        <head>
           <title>Test</title>
           <style>img{float:left;margin;spx;}</style>
        </head>
        <body>
        """)



        files = os.listdir(os.getcwd())
        for f in files:
            if f.lower().endswith('.jpeg') or f.lower().endswith('.png'):
                if picture in f:
                    html.write("time:%d:%d:%d" % (time.localtime().tm_hour,time.localtime().tm_min,time.localtime().tm_sec))
                    html.write("<p>%s</p>" % comment)
                    html.write("<img src='%s'>" % f)
       
        html.write('</body></html>')
        html.close()
        
        pass
        

    def read_file(self,fpath):
        BLOCK_SIZE =1024
        with open(fpath,'rb') as f:
            while True:
                block = f.read(BLOCK_SIZE)
                if block:
                    yield block
                else:
                    return

    def read_file_by_line(self,fpath):
        with open(fpath,'rb') as f:
            line = f.readline()
            while line:
                yield line
                line = f.readline()
            return

    def create_big_file(self,fpath):
        with open(fpath,'a') as f:
            for i in xrange(10000000000000):
                f.write("this is a test file %d \n" % (i) )
                print("%d" % (i))


    def debug(self):
        reader = self.read_file_by_line("/home/nfs/working/automation/script/bigfile.py")
        line = reader.next()
        print(line)
        while line:
            line = reader.next()
            print(line)
        pass

    def debug1(self):
        reader = self.create_big_file("/home/nfs/working/automation/script/bigfile.py")

    def debug2(self):
        with open("/home/nfs/working/automation/script/bigfile.py",'rb') as f:
            lines = f.readlines()
            for item in lines:
                print(item)


    def debug3(self):
        #print(dir(TestCaseFramework))
        print(TestCaseFramework.__dict__)


    def debug4(self):

        for i in range(109):
            self.screen_shot("comment"+str(i))
            print("bug.....%d" % i)


            

    def runTest(self):
        #self.mouse_click(1,39,1056)
        for i in range(150):
            self.screen_shot("comment"+str(i))
            print("bug.....%d" % i)
        #self.mouse_location()
        #self.open_app("gimp")
        #print("hello")
        
        pass





if __name__ == "__main__":


    suite=unittest.TestSuite()
    #suite.addTest(TestCaseFramework("runTest"))
    suite.addTest(TestCaseFramework("debug4"))
    runner = unittest.TextTestRunner()
    runner.run(suite)

    sys.exit()

