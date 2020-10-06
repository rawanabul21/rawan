import os
from matplotlib import pyplot as plt
name='test11g'
file = os.path.join('C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\', name+'.txt')
print(file)
def extract_info(myline, list_left, list_top, list_width, list_height):
    if "Location:" in myline:
        t = myline.partition("Rect(")[2]
        t = t.partition(")")[0]

        # Getting left, top, width, height coordinates in list to graph seperatly
        left = t.partition("left=")[2]
        left = int(left.partition(", top")[0])
        list_left.append(left)

        top = t.partition("top=")[2]
        top = int(top.partition(", width")[0])
        list_top.append(top)

        width = t.partition("width=")[2]
        width = int(width.partition(", height")[0])
        list_width.append(width)

        height = t.partition("height=")[2]
        height = int(height.partition(")")[0])
        list_height.append(height)



#Graphing plot of tilt variation in coordinates
def graph(list_left,list_top,list_width, list_height, qr):
    x_left = range(0, len(list_left))
    x_top = range(0, len(list_top))
    x_width = range(0, len(list_width))
    x_height = range(0, len(list_height))

    fig, axs = plt.subplots(2, 2, figsize=(15.0, 8.0))
    axs[0, 0].plot(x_left, list_left)
    axs[0, 0].set_title('Tilt Variation in Left Coordinates')
    axs[0, 1].plot(x_top, list_top, 'tab:orange')
    axs[0, 1].set_title('Tilt Variation in Top Coordinates')
    axs[1, 0].plot(x_width, list_width, 'tab:green')
    axs[1, 0].set_title('Tilt variation in Width Coordinates')
    axs[1, 1].plot(x_height, list_height, 'tab:red')
    axs[1, 1].set_title('Tilt Variation in Height Coordinates')

    for ax in axs.flat:
            ax.set(xlabel='points', ylabel='variation')

    #fig.show()
    fig.savefig('C:\\Users\\Rawan\\PycharmProjects\\OCR_Thesis\\Data Collection\\graphs\\' + name + qr + '.png')

# extracting coordinate points in QR Tag detection from qr_code
#with open(file, 'rt') as myfile:
list_lefttr = []
list_toptr = []
list_widthtr = []
list_heighttr = []

list_lefttl = []
list_toptl = []
list_widthtl = []
list_heighttl = []

list_leftbl = []
list_topbl = []
list_widthbl = []
list_heightbl = []

qrtl = '_tl'
qrtr='_tr'
qrbl='_bl'

with open(file, 'r+') as f:
    lines = f.readlines()
    for i in range(0, len(lines)):
        line = lines[i]
        if "topright" in line:
            line = lines[i+1]
            extract_info(line, list_lefttr, list_toptr, list_widthtr, list_heighttr)
        elif "topleft" in line:
            line = lines[i+1]
            extract_info(line, list_lefttl, list_toptl, list_widthtl, list_heighttl)
        elif "bottomleft" in line:
            line = lines[i+1]
            extract_info(line, list_leftbl, list_topbl, list_widthbl, list_heightbl)
#file.close()

    # for myline in myfile:
    #     if myline != "\n":
    #         myline = myline.rstrip()
    #         if "topright\\nLocation:" in myline:
    #             extract_info(myline, list_lefttr, list_toptr, list_widthtr, list_heighttr)
    #             qr = 'tr'


if list_toptr != []:
    graph(list_toptr, list_toptr, list_widthtr, list_heighttr, qrtr)
if list_toptl:
    graph(list_toptl, list_toptl, list_widthtl, list_heighttl, qrtl)
if list_topbl:
    graph(list_toptl, list_toptl, list_widthtl, list_heighttl, qrbl)



