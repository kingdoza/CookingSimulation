#팀프로젝트
#골리앗버드이터 - 20232872김도원, 20233020박정은, 20231650조가연
#주제 : 음식만들기 게임




from tkinter import *
import random
import time
from PIL import ImageTk, Image#@@@@@@@@@@@@@@@@@

root = Tk()
root.title("숭실최고요리왕")
root.geometry("800x600+100+100")
root.resizable(False, False)





#----------게임 관련 변수----------
myTitle = ["서울최고요리왕", "도쿄최고요리왕", "멕시코최고요리왕"]  #스테이지 별 칭호

stages = [ ["소고기미역국", "제육볶음", "두부조림", 0],     #스테이지 별 음식
           ["긴삐라 코보", "초밥", "고기우동", 30000],
           ["La Cochinita Pibil", "코하우일라", "몰레 포블라노", 80000] ]

foods = {"소고기미역국" : ["미역", "소고기", "물", 5000],      #음식 별 레시피
         "제육볶음" : ["돼지고기", "고추장\n양념", "채소믹스", 6000],
         "두부조림" : ["두부", "고추장\n양념", 4000],

        "긴삐라 코보" : ["우엉", "식초", "감자", "참깨", 15000],
        "초밥" : ["회", "밥", "배합초", 14000],
        "고기우동" : ["돼지고기", "멸치육수", "면", "버섯", 14000],

         "La Cochinita Pibil" : ["돼지고기", "양파", "칠리", "바나나잎", "오렌지\n주스", 32000],
         "코하우일라" : ["또띠아", "닭고기", "토마토\n소스", "고수", 27000],
         "몰레 포블라노" : ["또띠아", "양파", "초콜릿", "필리페퍼", "참깨", 29000],
         }

gredients = ["모짜렐라\n치즈", "채소믹스", "두부", "밀웜", "다진마늘", "미역",   #선택가능한 모든 재료
             "와사비", "돼지고기", "물", "고추장\n양념", "소고기",
             "또띠아", "양파", "초콜릿", "필리페퍼", "참깨", "또띠아", "닭고기", "토마토\n소스",
             "고수", "양파", "칠리", "바나나잎", "오렌지\n주스", "청어", "짱돌",
             "나초", "민트초코", "김치", "된장", "우엉", "식초", "감자", "참깨",
             "회", "쌀밥", "배합초", "멸치육수", "면", "버섯"]
#random.shuffle(gredients)   #재료 목록 랜덤으로 뒤섞기
gredients.sort()             #재료 ㄱㄴㄷ순으로 정렬

maxStage = 3    #총 스테이지 수
stageNum = 0   #현재 스테이지
hintRemain = 3  #남은 힌트 수
canTimer = False        #타이머 실행를 위한 참거짓 변수
orderedFood = ""        #주문음식
myGredient = []         #선택한 재료 목록
totalMoney = 10000      #총매출
maxMoney = totalMoney   #최대 총매출(결과출력할때 필요)
startTime = time.time()
timeLimit = 12          #제한시간

#------------------------------





#----------맨처음 화면 관련 함수----------
def GameStart():    #게임시작 or 재시작
    global stageNum
    stageNum = 0
    gameFrame.pack_forget()
    endFrame.pack_forget()
    startFrame.pack()
#------------------------------



#----------레시피 화면 관련 함수----------
def ShowRecipe():   #본게임 시작 전 레시피 화면 보여주기
    startFrame.pack_forget()
    gameFrame.pack_forget()
    index = 0
    for child in labelFrame.winfo_children():
        if isinstance(child, Label) and index < len(stages[stageNum]) - 1:
            MakeFoodLabel(child, stages[stageNum][index])
        elif isinstance(child, Label):
            child.config(text="")
        index += 1
    titleLable.config(text=f"칭호 : [ {myTitle[stageNum]} ]")
    recipeFrame.pack()


def MakeFoodLabel(label, food):    #레시피 화면에서 음식 레이블 만들기, 레이블은 총 3개
    label.config(text="-- " + food + " --" + "\n\n\n")
    for info in foods[food]:
        currentText = label.cget("text")
        if isinstance(info, str):
            newText = currentText + str(foods[food].index(info) + 1) + ". " + info + "\n\n"
        else:
            newText = currentText + "\n\n" + str(format(info, ",")) + "원"
        label.config(text=newText)
#------------------------------

#----------본게임 관련 함수----------
def StartMainGame():    #본게임 시작하기
    endFrame.pack_forget()
    startFrame.pack_forget()
    recipeFrame.pack_forget()
    gameFrame.pack()
    gameFrame.propagate(0)
    global totalMoney
    moneyLabel.config(text="총매출\n" + str(format(totalMoney, ","))+"원")
    CheckExpansion()
    ResetHint()
    GetOrder()
    global canTimer
    if canTimer == True:
        UpdateTimer()
    canTimer = True
    
def GetOrder():   #음식 주문받기
    myGredientLabel.config(text="")
    global orderedFood
    orderedFood = random.choice(stages[stageNum][0:-1])
    foodMoney = foods[orderedFood][len(foods[orderedFood])-1]
    foodLabel.place(x= 380, y = 60)
    foodLabel.config(text=orderedFood + "\n" + str(format(foodMoney, ","))+"원")
    myGredient.clear()
    global startTime
    startTime = time.time()

def UpdateTimer():  #타이머 함수
    if canTimer == True:
        remainTime = startTime - time.time() + timeLimit
        if remainTime <= 0:
            GetMoney(False)
            GetOrder()
        else:
            timeLabel.config(text="▉"*int(60*remainTime/timeLimit))
    timeLabel.after(50, UpdateTimer)
    
def GetGredient(gredient):    #재료 버튼 누르면 해당 재료를 선택한 재료 목록에다가 집어넣기
    myGredient.append(gredient)
    currentText = myGredientLabel.cget("text")
    myGredientLabel.config(text=currentText + gredient + " . ")

def CanGetMoney():      #음식 내보내기 버튼 누르면 돈 획득 여부 판별하기
    canGet = True
    if len(foods[orderedFood])-1 != len(myGredient):
        canGet = False
    else:
        canGet = CheckMyRecipe()
    GetMoney(canGet)
    DelHint()
    GetOrder()

def GetMoney(canGet):      #참거짓 매개변수에 따라 돈 얻기
    global totalMoney
    foodInfo = foods[orderedFood]
    if canGet == True:
        totalMoney += foodInfo[len(foodInfo)-1]
    else:
        totalMoney -= foodInfo[len(foodInfo)-1]
        if totalMoney <= 0:
            GameOver()
    moneyLabel.config(text="총매출\n" + str(format(totalMoney, ","))+"원")
    global maxMoney
    if totalMoney > maxMoney:
        maxMoney = totalMoney
    if(stageNum < maxStage):
        CheckExpansion()

def CheckExpansion():   #돈에 따라 해외진출 버튼 활성화 OR 비활성화
    if stageNum + 1 < maxStage:
        expanCost = stages[stageNum + 1][len(stages[stageNum + 1]) - 1]
        expanButton.config(text="해외 진출\n-" + str(format(expanCost, ","))+"원")
        if(totalMoney >= expanCost):
            expanButton['state'] = NORMAL
        else:
            expanButton['state'] = DISABLED
    else:
        expanButton.config(text="-")
        expanButton['state'] = DISABLED

def ExpanFood():    #해외진출 버튼 누르면 작동
    global stageNum
    expanCost = stages[stageNum + 1][len(stages[stageNum + 1]) - 1]
    global totalMoney
    totalMoney -= expanCost
    stageNum += 1
    global canTimer
    canTimer = False
    ShowRecipe()
    ChangeImage()

def ChangeImage():  #해외진출 시 배경이미지를 나라에 맞게 바꿈
    if stageNum == 1:
        background_label.config(image=japan_image)
    elif stageNum == 2:
        background_label.config(image=mexico_image)

def CheckMyRecipe():     #내 재료 목록이랑 원래 재료 목록이랑 비교하기. 같으면 참, 다르면 거짓 반환
    for i in range(len(myGredient)):
        if myGredient[i] != foods[orderedFood][i]:
            return False
    return True

def ShowHint():     #힌트 버튼 누르면 힌트 보여주기
    global hintRemain
    hintRemain -= 1
    hintButton.config(text="힌트 보기\n" + str(hintRemain) + "회")
    hintText = ""
    for i in range(len(foods[orderedFood])-1):
        hintText += foods[orderedFood][i] + " . "
        hintLabel.config(text=hintText)
    if hintRemain == 0:
        hintButton['state'] = DISABLED
    
def ResetHint():    #스테이지 시작할때 힌트 초기화하기
    hintRemain = 3
    hintButton['state'] = NORMAL
    hintButton.config(text="힌트 보기\n" + str(hintRemain) + "회")

def DelHint():      #힌트 레이블 비우기
    hintLabel.config(text="")
    hintButton.config(text="힌트 보기\n" + str(hintRemain) + "회")
#------------------------------



#----------게임오버 이후 관련 함수----------
def GameOver():     #게임오버창 보여주기
    global totalMoney
    totalMoney = 10000
    global canTimer
    canTimer = False
    gameFrame.pack_forget()
    hignMoneyLabel.config(text="--- 최고 매출 ---\n" + str(format(maxMoney, ","))+"원")
    endFrame.pack()
    background_label.config(image=korea_image)

def ExitGame():     #게임 종료
    root.destroy()
#------------------------------




#****************************이하 모두 tkinter 관련****************************

#----------화면 전환을 위한 프레임 선언----------
startFrame = Frame(root, width=800, height=600)     #맨처음 시작화면의 프레임
recipeFrame = Frame(root, width=800, height=600)    #레시피 화면의 프레임
gameFrame = Frame(root, width=800, height=600)      #본게임 프레임
endFrame = Frame(root, width=800, height=600)       #게임오버 프레임
#------------------------------




#----------시작화면 프레임 구성----------

#@@@@@@@@@@@@@@@@@@@
start_image = ImageTk.PhotoImage(Image.open("start.png"))
start_image_label = Label(startFrame)
start_image_label = Label(startFrame, image=start_image)
start_image_label.place(x=0, y=400)
start_image_label.pack()


string1 = "원도는 세계 여러 나라의 음식을 정복하고자 음식점을 개장했습니다.\n\n"      #맨처음 시작화면 문구
string2 = "상단에 표시되는 주문 음식에 맞게 레시피를 제한시간안에 클릭하세요.\n\n"
string3 = "성공적으로 음식을 완성하지못하면 화난 손님이 돈을 강탈합니다!\n\n"
string4 = "총매출이 0원이하면 원도는 벼락거지가 된 채 장사를 접게됩니다...\n\n"
string5 = "원도의 음식점을 키워주세요!\n\n"
totalString = "\n" + string1 + string2 + string3 + string4 + string5
openingLabel = Label(startFrame, text=totalString)    #원도 문구 레이블
openingLabel.pack()
gotoRecipeButton = Button(startFrame, text="게임시작", height=3, width=15, command=ShowRecipe)    #게임시작 버튼(레시피 화면으로 이동)
gotoRecipeButton.pack()

#------------------------------

#----------레시피 화면 프레임 구성---------

titleLable = Label(recipeFrame) #칭호 레이블
titleLable.pack()
labelFrame = Frame(recipeFrame) #3의 음식 레이블을 담을 프레임



for labelNum in range(1, 4):    
    recipeLabel = Label(labelFrame) #각각의 음식 레이블
    recipeLabel.grid(column=labelNum, row=0, padx=20, pady=5)
labelFrame.pack()


startbutton = Button(recipeFrame, text="게임시작", height=3, width=15, command=StartMainGame)    #본게임 시작 버튼
startbutton.pack(side="top", pady=20)
start2_image = ImageTk.PhotoImage(Image.open("start2.png"))
start2_image_label = Label(recipeFrame)
start2_image_label = Label(recipeFrame, image=start2_image)
start2_image_label.place(x=0, y=300)
start2_image_label.pack()

#------------------------------



#----------본게임 프레임 구성----------
#@@@@@@@@@@@@@@
korea_image = ImageTk.PhotoImage(Image.open("korea.png"))
japan_image = ImageTk.PhotoImage(Image.open("japan.png"))
mexico_image = ImageTk.PhotoImage(Image.open("mexico.png"))
background_label = Label(gameFrame)
background_label = Label(gameFrame, image=korea_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


foodLabel = Label(gameFrame, text="")   #주문음식 레이블
foodLabel.pack()
myGredientLabel = Label(gameFrame)      #선택한 재료 레이블
myGredientLabel.place(x=300, y=450)
moneyLabel = Label(gameFrame, text="총매출\n" + str(format(totalMoney, ","))+"원")  #총매출 레이블
moneyLabel.place(x=680,y=55)
expanButton = Button(gameFrame, text="해외 진출", height=3, width=15, command=ExpanFood)    #해외진출 버튼
expanButton.place(x=60,y=50)
timeLabel = Label(gameFrame)    #제한시간(사각형) 레이블
timeLabel.place(x=40, y=0)
buttonFrame = Frame(gameFrame)  #본게임 내 재료버튼을 묶어주는 프레임
buttonFrame.place(y=140)
hintButton = Button(gameFrame, text="힌트 보기\n" + str(hintRemain) + "회", height=2, width=10, command=ShowHint)   #힌트 버튼
hintButton.place(x=670,y=100)
hintLabel = Label(gameFrame)    #레시피 힌트 출력 레이블
hintLabel.place(x=540,y=100)

rowNum = 0
colNum = 0
for gredient in gredients:  #재료 버튼 배치하기
    button = Button(buttonFrame, text=gredient, height=2, width=10, command=lambda text=gredient: GetGredient(text)) #각각의 재료버튼
    button.grid(row=rowNum, column=colNum)
    colNum += 1
    if colNum >= 10:
        colNum = 0
        rowNum += 1

button = Button(gameFrame, text="음식 내보내기", height=3, width=15, command=CanGetMoney)   #음식내보내기 버튼
button.pack(side="bottom", pady=20)




#------------------------------




#----------게임오버 프레임 구성----------
end_image = ImageTk.PhotoImage(Image.open("end.png"))
end_image_label = Label(endFrame, image=end_image)
end_image_label.place(x=0, y=-100, relwidth=1, relheight=1)

endingLabel = Label(endFrame, text="[가게 폐점]\n\n원도는 벼락거지가 되었습니다...\n\n")    #엔딩 문구 레이블
endingLabel.place(x=320, y=380)
hignMoneyLabel = Label(endFrame)    #최고 매출 레이블
hignMoneyLabel.place(x= 360, y= 330)
restartButton = Button(endFrame, text="다시하기", height=3, width=15, command=GameStart)    #재시작 버튼
restartButton.place(x=290, y=440)
exitButton = Button(endFrame, text="종료하기", height=3, width=15, command=ExitGame)    #게임종료 버튼
exitButton.place(x=410, y=440)
#------------------------------



StartMainGame() #게임 시작
GameStart()

root.mainloop()
