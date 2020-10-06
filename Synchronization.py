import os
class Synchronization:

    def __init__(self, filepath, newFilename, logFile):
        self.filepath = filepath
        self.logFile = logFile
        self.sync(filepath, newFilename)

    def sync(self, filepath,  newFilename):
        # Getting list of timestamps from video
        list1 = []
        for filename in os.listdir(filepath):
            if filename.endswith('.jpg'):
                list1.append(filename.replace('.jpg', ''))
        for i in range(0, len(list1)):
            list1[i] = int(list1[i])
        list1.sort()

        # Getting list of timestamps from logfile
        with open(logFile, 'rt') as myfile:
            list2 = []
            for myline in myfile:
                if myline != "\n":
                    if "Accelerometer" in myline or "Gyroscope" in myline:
                        t = myline.partition("Time:")[2]
                        t = t.partition("\n")[0]
                    if "TouchData" in myline:
                        t = myline.partition("time_ms:")[2]
                        t = t.partition(";")[0]
                    list2.append(int(t))
            list2.sort()

            print(list1)
            print(list2)

            # creating a list of pairs of the two closest timestamps in log and video
            list3 = []
            for i in list2:
                j = self.closest(list1, i)
                print(j)
                list3.append([i, j])

            print(list3)
            self.addToFile(list3, newFilename)

    def write(self, filename, line):
        with open(filename, 'a') as the_file:
            the_file.write(line)

    #creats new Log file that contains the FramID # taken from video
    def addToFile(self, list, newFilename):
        for i,j in list:
            with open(logFile, 'rt') as myfile:
                for myline in myfile:
                    if myline != "\n":
                        #getting the timestamp info from log file
                        myline = myline.rstrip()
                        t1 = myline.partition("Time:")[2]
                        t1 = t1.partition("\n")[0]
                        t1 = t1.strip()
                        t2 = myline.partition("time_ms:")[2]
                        t2 = t2.partition(";")[0]
                        t2= t2.strip()
                        # checking if log file timestamps matches the one on the list
                        if t1 != '':
                            if str(i) == t1:
                                line = myline + "; frameID: " + str(j) + ".jpg" + "\n"
                                self.write(newFilename, line)
                        if t2 != '':
                            if str(i) == t2:
                                line = myline + "; frameID: " + str(j) +".jpg" + "\n"
                                self.write(newFilename, line)

    # find Closest number in a list
    def closest(self, lst, K):

        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - K))]

filepath = "Data Collection\\output_screenshots\\test17e_frames"
newFilename = os.path.join('Data Collection\\LogData_Edited', 'logEntryEdited17e.txt')
logFile = os.path.join('Data Collection\\LogData', 'logEntryData17e.txt')
Synchronization(filepath, newFilename, logFile)