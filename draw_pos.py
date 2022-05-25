import cv2
import numpy as np

# 本代码的功能是在图片通过点击获得点击位置
# 在本项目中用于找段首区间，栏宽，底边等位置
# 需要设置图片的 名字name 和 相对路径path
# 按 q 结束运行并把 本图片保存在 set_pos 目录下
name = 'image00099.jpg'
path = 'images/99-206/'
save_path = "set_pos/"

img=cv2.imread(path+name)

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 2, (255, 0, 0), thickness = 4)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    2.0, (0,0,255), thickness = 4)
        cv2.imshow("image", img)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
while(1):
    #cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)
    k = cv2.waitKey(0)
    if ord('q') == k:
        cv2.imwrite(save_path + name,img)
        break
cv2.destroyAllWindows()
