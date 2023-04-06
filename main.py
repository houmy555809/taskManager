try:
    from tkinter import *
    from datetime import *
    import time
    from sys import *
    from functools import cmp_to_key
    root=Tk()
    root.geometry("500x130-0-40")
    root.resizable(False,False)
    root.overrideredirect(True)
    root.attributes("-alpha",0.75)
    schedule=[
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
    warn_stv=StringVar(root,"")
    warn=Label(root,textvariable=warn_stv,font=("Consolas",15),fg="black")
    warn.pack()
    stv=StringVar(root,"")
    lbl=Label(root,textvariable=stv,font=("Consolas",30))
    lbl.pack()
    def show_notice(txt):
        ntc=Tk();
        ntc.geometry("500x45-5-500")
        ntc.overrideredirect(True)
        txt=Label(ntc,text="通知："+txt,font=(40))
        txt.pack();
        ntc.attributes("-topmost",True)
        alpha=1.0
        x,y=0,0
        def disappear():
            nonlocal alpha
            alpha-=0.05
            ntc.attributes("-alpha",alpha)
            if alpha<=0.05:
                ntc.destroy()
            ntc.after(20,disappear)
        ntc.after(2500,disappear)
    def front():
        root.attributes('-topmost',True)
        root.after(10,front)
    def is_after(a,b):
        if a[0]!=b[0]:
            return a[0]>b[0]
        if a[1]!=b[1]:
            return a[1]>b[1]
        if a[2]!=b[2]:
            return a[2]>b[2]
    def time_sub(a,b):
        ans=[0,0,0]
        ans[0]+=a[0]-b[0]
        if a[1]<b[1]:
            ans[0]-=1
            ans[1]+=60
        ans[1]+=a[1]-b[1]
        if a[2]<b[2]:
            ans[1]-=1
            ans[2]+=60
        ans[2]+=a[2]-b[2]
        return tuple(ans)
    def refresh():
        time=datetime.today()
        ctime=(time.hour,time.minute,time.second)
        flag=False
        nxt=None
        for i in schedule[time.weekday()]:
            if is_after(i[1],ctime):
                dt=time_sub(i[1],ctime)
                if dt[0]==0 and dt[1]==1 and dt[2]==0:
                    show_notice("距离 "+i[0]+" 开始还有1分钟，请做好准备")
                if dt[0]==0 and dt[1]==0 and dt[2]==5:
                    show_notice("事项 "+i[0]+" 即将开始，请做好准备")
            if not is_after(i[1],ctime) and is_after(i[2],ctime):
                timebefore=time_sub(i[2],ctime)
                str_tm="距离结束"
                if timebefore[0]>0:
                    str_tm+=str(timebefore[0])+"小时"
                if timebefore[1]>0:
                    str_tm+=str(timebefore[1])+"分钟"
                if timebefore[2]>0:
                    str_tm+=str(timebefore[2])+"秒"
                warn_stv.set(str_tm)
                if time.hour>=10:
                    timestr=str(time.hour)
                else:
                    timestr="0"+str(time.hour)
                timestr+=":"
                if time.minute>=10:
                    timestr+=str(time.minute)
                else:
                    timestr+="0"+str(time.minute)
                timestr+=":"
                if time.second>=10:
                    timestr+=str(time.second)
                else:
                    timestr+="0"+str(time.second)
                stv.set(timestr+"\n当前事项："+i[0])
                flag=True
            elif is_after(i[1],ctime):
                if nxt==None:
                    nxt=i
        if not flag:
            if time.hour>=10:
                timestr=str(time.hour)
            else:
                timestr="0"+str(time.hour)
            timestr+=":"
            if time.minute>=10:
                timestr+=str(time.minute)
            else:
                timestr+="0"+str(time.minute)
            timestr+=":"
            if time.second>=10:
                timestr+=str(time.second)
            else:
                timestr+="0"+str(time.second)
            stv.set(timestr+"\n当前无事项")
            if nxt!=None:
                str_tm="下一事项："+nxt[0]+"  距离开始"
                timebefore=time_sub(nxt[1],ctime)
                if timebefore[0]>0:
                    str_tm+=str(timebefore[0])+"小时"
                if timebefore[1]>0:
                    str_tm+=str(timebefore[1])+"分钟"
                if timebefore[2]>0:
                    str_tm+=str(timebefore[2])+"秒"
            else:
                str_tm="今日无事项"
            warn_stv.set(str_tm)
        root.after(100,refresh)
    root.after(10,front)
    root.after(100,refresh)
    x,y=0,0
    def load():
        def cmp(x,y):
            if(is_after(x[1],y[1])):
                return 1
            elif(is_after(y[1],x[1])):
                return -1
            else:
                return 0
        with open("schedule.txt","r",encoding="UTF-8") as file:
            for s in file.readlines():
                try:
                    s=s.strip("\r\n")
                    s=s.split(" ")
                    trs={"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
                    day=trs[s[0]]
                    name=s[1]
                    st=s[2].split(":")
                    en=s[3].split(":")
                    st[0],st[1],st[2]=int(st[0]),int(st[1]),int(st[2])
                    en[0],en[1],en[2]=int(en[0]),int(en[1]),int(en[2])
                    schedule[day].append([name,st,en])
                except:
                    pass
            file.close()
        for i in range(7):
            schedule[i].sort(key=cmp_to_key(cmp))
    def mouse_motion(event):
        global x,y
        offset_x,offset_y=event.x-x,event.y-y  
        new_x=root.winfo_x()+offset_x
        new_y=root.winfo_y()+offset_y
        new_geometry=f"+{new_x}+{new_y}"
        root.geometry(new_geometry)
    def mouse_press(event):
        global x,y
        count=time.time()
        x,y=event.x,event.y
    def close(event):
        root.destroy()
    def settings(event):
        settings=Tk()
        settings.title("设置")
        settings.geometry("500x500")
        dat=[]
        objs=[]
        stringvars=[]
        delbtns=[]
        def save(event):
            with open("schedule.txt","w",encoding="UTF-8") as file:
                file.truncate(0)
                file.write("\n".join(dat));
                file.close()
            load()
        save_btn=Label(settings,text="📥")
        save_btn.bind("<Button-1>",save)
        save_btn.place(x=480,y=5)
        save_btn["cursor"]="hand2"
        def msin_savebtn(event):
            save_btn["fg"]="white"
            save_btn["bg"]="lightgray"
        def msot_savebtn(event):
            save_btn["fg"]="black"
            save_btn["bg"]="white"
        save_btn.bind("<Enter>",msin_savebtn)
        save_btn.bind("<Leave>",msot_savebtn)
        lbl_row1=Label(settings,text="星期几")
        lbl_row1.place(x=20,y=10)
        lbl_row2=Label(settings,text="任务名称")
        lbl_row2.place(x=70,y=10)
        lbl_row3=Label(settings,text="开始时间")
        lbl_row3.place(x=150,y=10)
        lbl_row4=Label(settings,text="结束时间")
        lbl_row4.place(x=240,y=10)
        def update():
            nonlocal stringvars,objs,delbtns,dat
            dat=[]
            for i in range(len(objs)):
                dat.append(stringvars[i][0].get()+" "+stringvars[i][1].get()+" "+stringvars[i][2].get()+":"+stringvars[i][3].get()+":"+stringvars[i][4].get()+
                           " "+stringvars[i][5].get()+":"+stringvars[i][6].get()+":"+stringvars[i][7].get())
            settings.after(100,update)
        settings.after(100,update)
        def delete(i):
            nonlocal stringvars,objs,delbtns,dat
            for idx in objs:
                for j in idx:
                    j.destroy()
            for idx in delbtns:
                idx.destroy()
            stringvars=[]
            objs=[]
            delbtns=[]
            del dat[i]
            for dt in dat:
                set(dt)
        def add():
            stringvars.append([StringVar(settings,"Mon"),StringVar(settings,"None"),StringVar(settings,"00"),StringVar(settings,"00"),
                        StringVar(settings,"00"),StringVar(settings,"24"),StringVar(settings,"00"),StringVar(settings,"00")])
            objs.append([Entry(settings,textvariable=stringvars[-1][0]),#weekday
                         Entry(settings,textvariable=stringvars[-1][1]),#name
                         Entry(settings,textvariable=stringvars[-1][2]),#start
                         Label(settings,text=":"),
                         Entry(settings,textvariable=stringvars[-1][3]),
                         Label(settings,text=":"),
                         Entry(settings,textvariable=stringvars[-1][4]),
                         Entry(settings,textvariable=stringvars[-1][5]),#end
                         Label(settings,text=":"),
                         Entry(settings,textvariable=stringvars[-1][6]),
                         Label(settings,text=":"),
                         Entry(settings,textvariable=stringvars[-1][7])])
            delbtns.append(Button(settings,text="-",command=lambda i=len(objs)-1:delete(i)))
            ypos=len(objs)*20+15
            objs[-1][0].place(x=20,y=ypos,width=30,height=15)
            
            objs[-1][1].place(x=70,y=ypos,width=70,height=15)
            
            objs[-1][2].place(x=150,y=ypos,width=20,height=15)
            objs[-1][3].place(x=170,y=ypos,width=10,height=15)
            objs[-1][4].place(x=180,y=ypos,width=20,height=15)
            objs[-1][5].place(x=200,y=ypos,width=10,height=15)
            objs[-1][6].place(x=210,y=ypos,width=20,height=15)
            
            objs[-1][7].place(x=240,y=ypos,width=20,height=15)
            objs[-1][8].place(x=260,y=ypos,width=10,height=15)
            objs[-1][9].place(x=270,y=ypos,width=20,height=15)
            objs[-1][10].place(x=290,y=ypos,width=10,height=15)
            objs[-1][11].place(x=300,y=ypos,width=20,height=15)
            
            delbtns[-1].place(x=350,y=ypos,width=15,height=15)
        def set(st):
            add()
            
            st=st.split()
            stringvars[-1][0].set(st[0])
            stringvars[-1][1].set(st[1])
            
            start=st[2].split(":")
            stringvars[-1][2].set(start[0])
            stringvars[-1][3].set(start[1])
            stringvars[-1][4].set(start[2])
            
            end=st[3].split(":")
            stringvars[-1][5].set(end[0])
            stringvars[-1][6].set(end[1])
            stringvars[-1][7].set(end[2])
        def addnw(event):
            set("Mon 未命名 00:00:00 00:00:00")
        add_btn=Label(settings,text="+")
        add_btn.bind("<Button-1>",addnw)
        add_btn["cursor"]="hand2"
        add_btn.place(x=350,y=10)
        def msin_addbtn(event):
            add_btn["fg"]="white"
            add_btn["bg"]="lightgrey"
        def msot_addbtn(event):
            add_btn["fg"]="black"
            add_btn["bg"]="white"
        add_btn.bind("<Enter>",msin_addbtn)
        add_btn.bind("<Leave>",msot_addbtn)
        with open("schedule.txt","r",encoding="UTF-8") as f:
            for i in f.readlines():
                try:
                    set(i)
                    dat[-1]=i
                except Exception as e:
                    print(e)
            f.close()
    
    close_btn=Label(root,text=" X ")
    close_btn.bind("<Button-1>",close)
    close_btn.place(x=480,y=5)
    close_btn["cursor"]="hand2"
    def msin_closebtn(event):
        close_btn["fg"]="white"
        close_btn["bg"]="red"
    def msot_closebtn(event):
        close_btn["fg"]="black"
        close_btn["bg"]="white"
    close_btn.bind("<Enter>",msin_closebtn)
    close_btn.bind("<Leave>",msot_closebtn)
    
    setting_btn=Label(root,text="⚙")
    setting_btn.bind("<Button-1>",settings)
    setting_btn.place(x=460,y=5)
    setting_btn["cursor"]="hand2"
    def msin_settingbtn(event):
        setting_btn["fg"]="white"
        setting_btn["bg"]="lightgray"
    def msot_settingbtn(event):
        setting_btn["fg"]="black"
        setting_btn["bg"]="white"
    setting_btn.bind("<Enter>",msin_settingbtn)
    setting_btn.bind("<Leave>",msot_settingbtn)
    
    root.bind("<B1-Motion>",mouse_motion)
    root.bind("<Button-1>",mouse_press) 
    load()
    root.mainloop()
except Exception as e:
    print(e)
    input("出现错误，请按回车键关闭。")
