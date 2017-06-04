# SHU-XK-Deamon

上海大学 选课系统 自动选课守护<br />

Thanks to the inspiration from [Lodour's](https://github.com/Lodour/SHU-XK) and [Diggerdu's](https://github.com/diggerdu/Shanghai-University-Course-Kit) Repo

Write this because of growing course proxy in xk.shu.edu.cn and more restricted system environment

I'm not sure but indeed we need a tool that is strong enough grasping courses day and night.

However to jump over the validate code is not a small case. 

Diggerdu uses initially SVM and then RNN which finally reach 90%+ correctness.

Unfortunately he uses bunches of dependencys that I can't resolve.

and You can use this script with less dependencys to resolve.

-----
usage
-----
1. $sudo pip3 install pillow pytesseract
2. $sudo apt install tesseract-ocr
3. $git clone https://github.com/lonelam/SHU-XK-Deamon.git
4. $cd SHU-XK-Deamon
5. Create and modify 'config.ini'.
6. $nohup python3 query_class.py &

-----
config.ini
-----
	[user]
	username:151234567
	password:12345678
	[courses]
	course_list:['08306030',]
	teacher_ids:['1002',]

bug反馈:diggerdu@hotmail.com<br />
