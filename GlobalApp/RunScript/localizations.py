import importlib
import sys
import os
import glob
import string
import os
import re
import time

importlib.reload(sys)
# sys.setdefaultencoding('utf-8')

kSourceFile = 'Base.lproj/*.storyboard'

kTargetFile = '*.lproj/*.strings'

kGenerateStringsFile = 'B.strings'

ColonRegex = u'["](.*?)["]'

KeyParamRegex = u'["](.*?)["](\s*)=(\s*)["](.*?)["];'

AnotationRegexPrefix = u'/(.*?)/'


def constructAnotationRegex(str):
    return AnotationRegexPrefix + '\n' + str


def getAnotationOfString(string_txt, suffix):
    anotationRegex = constructAnotationRegex(suffix)
    anotationMatch = re.search(anotationRegex, string_txt)
    anotationString = ''
    if anotationMatch:
        match = re.search(AnotationRegexPrefix, anotationMatch.group(0))
        if match:
            anotationString = match.group(0)
    return anotationString


def compareWithFilePath(newStringPath, originalStringPath):
    # read newStringfile
    with open(newStringPath, "r", encoding='utf-8', errors='ignore') as nspf:
        newString_txt = str(nspf.read(5000000))
    newString_dic = {}
    anotation_dic = {}
    print(newString_txt)
    for stfmatch in re.finditer(KeyParamRegex, newString_txt):
        linestr = stfmatch.group(0)
        anotationString = getAnotationOfString(newString_txt, linestr)
        linematchs = re.findall(ColonRegex, linestr)
        if len(linematchs) == 2:
            leftvalue = linematchs[0]
            rightvalue = linematchs[1]
            newString_dic[leftvalue] = rightvalue
            anotation_dic[leftvalue] = anotationString

    # read originalStringfile
    with open(originalStringPath, "r", encoding='utf-8', errors='ignore') as ospf:
        originalString_txt = str(ospf.read(5000000))
    originalString_dic = {}
    for stfmatch in re.finditer(KeyParamRegex, originalString_txt):
        linestr = stfmatch.group(0)
        linematchs = re.findall(ColonRegex, linestr)
        if len(linematchs) == 2:
            leftvalue = linematchs[0]
            rightvalue = linematchs[1]
            originalString_dic[leftvalue] = rightvalue

    # compare and remove the useless param in original string
    for key in originalString_dic:
        if (key not in newString_dic):
            keystr = '"%s"' % key
            replacestr = '//' + keystr
            match = re.search(replacestr, originalString_txt)
            if match is None:
                originalString_txt = originalString_txt.replace(keystr, replacestr)

    #compare and add new param to original string
    executeOnce = 1
    for key in newString_dic:
        if (key not in originalString_dic):
            values = (key, newString_dic[key])
            newline = ''
            if executeOnce == 1:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                newline = '\n//##################################################################################\n'
                newline += '//#           AutoGenStrings            ' + timestamp + '\n'
                newline += '//##################################################################################\n'
                executeOnce = 0
            newline += '\n' + anotation_dic[key]
            newline += '\n"%s" = "%s";\n' % values
            originalString_txt += newline
    # write into origial file
    sbfw = open(originalStringPath, "w")
    sbfw.write(originalString_txt)
    sbfw.close()


def extractFilePrefix(file_path):
    seg = file_path.split('/')
    lastIndex = len(seg) - 1
    return seg[lastIndex].split('.')[0]


def extractFileName(file_path):
    seg = file_path.split('/')
    lastIndex = len(seg) - 1
    return seg[lastIndex]


def generateStoryboardStringsfile(storyboard_path, tempstrings_path):
    cmdstring = 'ibtool ' + storyboard_path + ' --generate-strings-file ' + tempstrings_path
    if os.system(cmdstring) == 0:
        return 1


def main():
    filePath = sys.argv[1]
    sourceFilePath = filePath + '/' + kSourceFile
    sourceFile_list = glob.glob(sourceFilePath)
    if len(sourceFile_list) == 0:
        print('error directory, you should choose the dir upper the Base.lproj')
        return
    print(sourceFile_list)
    targetFilePath = filePath + '/' + kTargetFile
    targetFile_list = glob.glob(targetFilePath)
    tempFile_Path = filePath + '/' + kGenerateStringsFile
    if len(targetFile_list) == 0:
        print('error framework, no .lproj dir was found')
        return
    for sourcePath in sourceFile_list:
        sourcePrefix = extractFilePrefix(sourcePath)
        sourceName = extractFileName(sourcePath)
        print('create with ' + sourceName)
        if generateStoryboardStringsfile(sourcePath, tempFile_Path) == 1:
            print('- - genstrings %s successfully' % sourceName)
            for targetPath in targetFile_list:
                targetPrefix = extractFilePrefix(targetPath)
                targetName = extractFileName(targetPath)
                if sourcePrefix == targetPrefix:
                    print('- - dealing with %s' % targetPath)
                    compareWithFilePath(tempFile_Path, targetPath)
            print('finish with %s' % sourceName)
#            os.remove(tempFile_Path)
        else:
            print('- - genstrings %s error' % sourceName)


if __name__ == '__main__':
    main()
