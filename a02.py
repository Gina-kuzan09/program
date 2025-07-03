import cv2
import os
import numpy as np
import keyboard


#キーボードのキーによる数字の割り当て
print("最大個数をキーボードのキーを使ってキャプチャを起動した後に入力して下さい")
print("キーボードのキー　｜　対応する数字")
print("　  ↑↓←→　　　　　　　　　0～3")
print("　 F1～F12                4～15")
print("　  #$%&                  35～38")
print("    ()*+                  40～43")
print("　　0～9　　　　　　　　　48～57")
print("　　A～Z　　　　　　　　　65～90")
print("　　a～z　　　　　　　　　97～122")
print("")
print("キャプチャを起動します")
cap = cv2.VideoCapture(0) #キャプチャ起動  0はPCのカメラ　1はウェブカメラ
ret,frame = cap.read() #キャプチャ取得
cv2.imshow("camera",frame) #キャプチャ表示

#最大個数の入力
while True:
    key1 = cv2.waitKey(1) & 0xFFFF #キーボードのキー入力
    event = keyboard.read_event() #キーボードのイベントの読み取り
    key_name1 = event.name #押されたキーの取得
    print("最大個数:")

    if key1 < 0:
        continue
    else:
        if  key_name1 == "up": #上矢印キー
            key1 = 0
        elif  key_name1 == "down": #下矢印キー
            key1 = 1
        elif  key_name1 == "left": #左矢印キー
            key1 = 2
        elif  key_name1 == "right": #右矢印キー
            key1 = 3
        elif  key_name1 == "f1": #F1キー
            key1 = 4
        elif  key_name1 == "f2": #F2キー
            key1 = 5
        elif  key_name1 == "f3": #F3キー
            key1 = 6
        elif  key_name1 == "f4": #F4キー
            key1 = 7
        elif  key_name1 == "f5": #F5キー
            key1 = 8
        elif  key_name1 == "f6": #F6キー
            key1 = 9
        elif  key_name1 == "f7": #F7キー
            key1 = 10
        elif  key_name1 == "f8": #F8キー
            key1 = 11
        elif  key_name1 == "f9": #F9キー
            key1 = 12
        elif  key_name1 == "f10": #F10キー
            key1 = 13
        elif  key_name1 == "f11": #F11キー
            key1 = 14
        elif  key_name1 == "f12": #F12キー
            key1 = 15
        print(key1)
        break

#
cap = cv2.VideoCapture(0) #キャプチャ起動　 0はPCのカメラ　1はウェブカメラ

#カメラを使用して円を検出する処理
while True:
   count = 0 #円の検出数
   white = 0 #白色の個数
   green = 0 #緑色の個数
   orange = 0 #オレンジ色の個数
   ret,frame = cap.read()
   cv2.imshow("camera",frame)
   key3 =cv2.waitKey(10)
   if key3 == 32:
      img = frame
      img_gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      img_gray1 = cv2.medianBlur(img_gray1 ,3)
      img_gray1 = cv2.equalizeHist(img_gray1)
      circles1 = cv2.HoughCircles(img_gray1, cv2.HOUGH_GRADIENT, dp=1, minDist=40, param1=100, param2=50, minRadius=70, maxRadius=120)
      #円の検出を行う
      if circles1 is not None:

          #1回目の円を検出し、マスクを作成
          for i in circles1[0].astype('uint16'):
              cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
              center = (i[0], i[1])#中心の座標
              radius = i[2]#半径
              mask = np.zeros_like(img)#マスク画像の作成
              cv2.circle(mask, center, radius, (255, 255, 255), -1)#指定した円の領域をマスクに描画
              masked_img = cv2.bitwise_and(img, mask)#指定した円の内部の抽出
              img_gray2 = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
              img_gray2 = cv2.medianBlur(img_gray2 ,3)
              img_gray2 = cv2.equalizeHist(img_gray2)
              circles2 = cv2.HoughCircles(img_gray2, cv2.HOUGH_GRADIENT, dp=1.1, minDist=20, param1=100, param2=50, minRadius=20, maxRadius=50)

              #作成したマスクで2回目の円を検出し、マスクを作成
              if circles2 is not None:
                 for x in circles2[0].astype('uint16'):
                     cv2.circle(img,(x[0],x[1]),x[2],(0,0,255),2)
                     center1 = (x[0], x[1])#中心の座標
                     radius1 = x[2]#半径
                     mask1 = np.zeros_like(masked_img)#マスク画像の作成
                     cv2.circle(mask1, center1, radius1, (255, 255, 255), -1)#指定した円の領域をマスクに描画
                     masked_img1 = cv2.bitwise_and(masked_img, mask1)#指定した円の内部の抽出

                     #キャップの色の色別(今回は白、オレンジ、緑で行い、ピクセル数の多さでキャップの色を判別)
                     #HSV色空間に変換
                     hsv = cv2.cvtColor(masked_img1, cv2.COLOR_BGR2HSV)

                     #白色の色範囲を設定
                     lower_white = np.array([0, 0, 200])  # 色の下限
                     upper_white = np.array([180, 55, 255])  # 色の上限
                     color_mask_white = cv2.inRange(hsv, lower_white, upper_white)  # 範囲内にある色を検出し、マスクを作成

                     #オレンジ色の色範囲を設定
                     lower_orange = np.array([10, 100, 20])  # 色の下限
                     upper_orange = np.array([25, 255, 255])  # 色の上限
                     color_mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)  # 範囲内にある色を検出し、マスクを作成

                     #緑色の色範囲を設定
                     lower_green = np.array([35, 100, 50])  # 色の下限
                     upper_green = np.array([85, 255, 150])  # 色の上限
                     color_mask_green = cv2.inRange(hsv, lower_green, upper_green)  # 範囲内にある色を検出し、マスクを作成

                     #各色のマスクを適用
                     result_white = cv2.bitwise_and(masked_img1, masked_img1, mask=color_mask_white)
                     result_orange = cv2.bitwise_and(masked_img1, masked_img1, mask=color_mask_orange)
                     result_green = cv2.bitwise_and(masked_img1, masked_img1, mask=color_mask_green)

                     #各色のピクセル数をカウント
                     white_count = cv2.countNonZero(color_mask_white)
                     orange_count = cv2.countNonZero(color_mask_orange)
                     green_count = cv2.countNonZero(color_mask_green)

                     #白とオレンジと緑のどれが多いかを判定　ピクセル数で比較
                     if white_count > orange_count and white_count>green_count:
                          dominant_mask = color_mask_white
                          dominant_color = "White"
                          white += 1
                     elif orange_count > green_count and orange_count > white_count:
                          dominant_mask = color_mask_orange
                          dominant_color = "Orange"
                          orange += 1
                     else:
                          dominant_mask = color_mask_green
                          dominant_color = "Green"
                          green += 1
    
                     #各色のマスクを結合
                     #combined_mask = cv2.bitwise_or(color_mask_white, color_mask_orange)
                     #combined_mask = cv2.bitwise_or(combined_mask, color_mask_green)

                     #結合されたマスクを適用
                     result_combined = cv2.bitwise_and(masked_img1,masked_img1, mask=dominant_mask) 
              
                     #円のマスクを作成
                     mask1 = np.zeros_like(img_gray2)
                     cv2.circle(mask1, center1, radius1, 255, -1)
    
                     #マスクを使って色を抽出
                     masked_img1 = cv2.bitwise_and(masked_img1,masked_img1, mask = mask1)
                     count += 1

          #マスクに文字を入れる
          cv2.putText(img, str(count) ,(0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
          cv2.putText(img, "water" ,(240, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 5, cv2.LINE_AA)  #白色
          cv2.putText(img, str(white) ,(330, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
          cv2.putText(img, "hot" ,(390, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 150, 255), 5, cv2.LINE_AA)    #オレンジ色
          cv2.putText(img, str(orange) ,(460, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
          cv2.putText(img, "tea" ,(500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 5, cv2.LINE_AA)      #緑色
          cv2.putText(img, str(green) ,(570, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)

          #最大個数になった場合
          if key1 == count:
             cv2.putText(img, 'clear' ,(70, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5, cv2.LINE_AA)
          else:
             cv2.putText(img, 'false' ,(80, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)


          #各色の色のマスクと各色の色を合成したマスクの表示
          #cv2.imshow('White Mask', result_white)
          #cv2.imshow('Orange Mask', result_orange)
          #cv2.imshow('Green Mask', result_green)
          #cv2.imshow('Detected Color', result_combined)

          #結果表示
          cv2.imshow('Masked Image', masked_img)
          cv2.imshow('Masked Image1', masked_img1)
          cv2.imshow("camera",img)
          cv2.waitKey()
          cv2.destroyAllWindows()