#TO DO
#1. OS System Path
#2. ZipFile Pass Cracker

import time
import os
import zipfile
import hashlib
import sys
import itertools

alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()'

class Wordlist():

    def __init__(self,repeat,repeatStart,chars,**kwargs):

        self.chars=chars
        self.repeat=repeat
        self.repeatStart=repeatStart
        
        for name,value in kwargs.items():
            if name=='charList':
                self.charList=value

            else:
                self.charList=None

    def generator(self):
        char1=alphabet.index(self.chars[0])
        char2=alphabet.index(self.chars[1])+1
        
        for z in range(self.repeatStart,self.repeat+1):
            for i in itertools.product((alphabet[a] for a in range(char1,char2)), repeat=z):
                i=''.join(i)
                yield i

    def generator2(self):
        for z in range(self.repeatStart,self.repeat+1):
            for i in itertools.product(self.charList,repeat=z):
                i=''.join(i)
                yield i

    def hash(self,generator,hashAlg):
        for word in generator:
            hasher=hashAlg(word.encode())
            hashes=hasher.hexdigest()
            yield hashes
        
def createWordlist(repeat,repeatStart,chars,charList):
    wordlist=Wordlist(repeat,repeatStart,chars,charList=charList)

    filename=input('\nEnter filename here: ')
    
    file=open('wordlists/'+filename+'.txt','w')
    file2=open('wordlists/'+filename+'HashIndex.txt','w')
    file3=open('wordlists/'+filename+'Hashes.txt','w')
    

    if wordlist.chars!=[]:
        for _hash,word in zip(wordlist.hash(wordlist.generator(),hashlib.md5),wordlist.generator()):
            file.write(word+'\n')
            print(word+': '+_hash)
            file2.write(word+': '+_hash+'\n')
            file3.write(_hash+'\n')

    else:
        for _hash,word in zip(wordlist.hash(wordlist.generator2(),hashlib.md5),wordlist.generator2()):
            file.write(word+'\n')
            print(word+': '+_hash)
            file2.write(word+': '+_hash+'\n')
            file3.write(_hash+'\n')

    file.close()
    file2.close()
    file3.close()

class ZipCracker():
    def __init__(self,file,wordlist):
        try:
            self.file=zipfile.ZipFile(os.path.join('zip',file))
        except IOError:
            print('\nERROR:\nNO SUCH FILE FOUND, RESTARTING...')
            time.sleep(1)
            Start(False)
            
            
        self.wordlist=wordlist

    def crack(self):
        correct_password=''
        for word in self.wordlist.readlines():
            password=word.strip('\n')
            try:
                self.file.extractall(os.path.join('zip','extracted'),pwd=password.encode())
                print('\nThe password is: '+password+'\n')
                correct_password=password

            except:
                if correct_password=='':
                    print('\nPassword "'+password+'" failed')
                pass

def Start(first_time):
    if first_time==True:
        name='#-_Gh0st_P4$$_H4CK_-#'
        print('#'*len(name)+'\n'+name+'\n'+'#'*len(name))

    menu_name='* MA1N M3NU *'
    print('\n'+'*'*len(menu_name)+'\n'+menu_name+'\n'+'*'*len(menu_name))
        
    try:
        action=int(input('\nWhat would you like to do?\n1.Create wordlist\n2.Crack password\n3.Exit\nEnter command here:'))
        
        if action>3:
            print('\nERROR: Choice must be one of the given numeral values!\n')
            print('RESTARTING...')
            Start(False)

    except ValueError:
        print('\nERROR: Choice must be one of the given numeral values!\n')
        print('RESTARTING...')
        Start(False)

    if action==1:
        try:
            wordlist_type=int(input('\nWould you like to:\n1.Create a specific character set\n2.Use a built-in alphabet\n3.Return to main menu\nEnter command here: '))

        except ValueError:
            print('\nERROR: Choice must be one of the given numeral values!\n')
            print('RESTARTING...')
            Start(False)
            
        if wordlist_type==1:
            charList_input=input('\nEnter your characters: ')
            charList=[]
            chars=[]
            
            for char in charList_input:
                charList.append(char)
                
        elif wordlist_type==2:
            char1=input('\nEnter the first character: ')
            char2=input('Enter the second character: ')

            try:
                char1[1]
                print('\nERROR: Choice must be one of the given numeral values!\n')
                print('RESTARTING...')
                Start(False)
                
            except IndexError:
                try:
                    char2[1]
                    print('\nERROR: Choice must be one of the given numeral values!\n')
                    print('RESTARTING...')
                    Start(False)

                except IndexError:
                    chars=[char1,char2]
                    charList=[]
                    
        elif wordlist_type==3:
            Start(False)
            
        else:
            print('\nERROR: Choice must be one of the given numeral values!\n')
            print('RESTARTING...')
            Start(False)

        try:
            repeat=int(input('\nHow long should the wordlist combinations be?\nEnter value here: '))
            repeatDeterminator=int(input('\nShould the combinations be:\n1.Exactly '+str(repeat)+' characters long\n2.Everything under '+str(repeat)+' characters including '+str(repeat)+' characters long\nInput choice here: '))

            if repeatDeterminator>2:
                print('\nERROR: Choice must be one of the given numeral values!\n')
                print('RESTARTING...')
                Start(False)

            elif repeatDeterminator==2:
                repeatStart=0

            else:
                repeatStart=repeat

            createWordlist(repeat,repeatStart,chars,charList)
                
        except ValueError:
            print('\nERROR: Choice must be one of the given numeral values!\n')
            print('RESTARTING...')
            Start(False)

    elif action==2:
        print('\nWould you like to: \n1.Crack a zip file password\n')
        try:
            action2=int(input('Enter command here: '))
            
            if action2>1 or action2<1:
                print('\nERROR: Choice must be one of the given numeral values!\n')
                print('RESTARTING...')
                Start(False)             
            elif action2==1:
                print('\nPlease put the zip file into the "zip" folder\n')
                filename=input('Enter zip filename: ')
                file=(filename+'.zip')
                wordlistName=input('Enter wordlist filename: ')
                try:
                    wordlist=open(os.path.join('wordlists',wordlistName+'.txt'))
                except IOError:
                    print('\nERROR:\nFILE NOT FOUND,RESTARTING...')
                    time.sleep(1)
                    Start(False)
                    
                    
                ZIP=ZipCracker(file,wordlist)
                ZIP.crack()
                
        except ValueError:
            print('\nERROR: Choice must be one of the given numeral values!\n')
            print('RESTARTING...')
            Start(False)
                    
Start(True)
input('\nPress ENTER to exit')
