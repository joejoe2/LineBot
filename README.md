# LineBot

basic instructions:
1.[gotcha]     (simulate gotcha in fate grand order)
[gotcha] -> 單抽

[gotcha]10 -> 十連抽(有保底四星禮裝或從者)

[gotcha]show -> 顯示你目前的抽卡結果統計

[gotcha]star3 -> 單抽,只抽三星

[gotcha]star4 -> 單抽,只抽三星

[gotcha]star5 -> 單抽,只抽三星

2.[luis]+something to say  (chineese only)

connected with azure luis for some greeting languge and reply from some templates

ex. [luis]幾點了? -> then bot will reply current time

ex. [luis]早安阿 -> then bot will reply 

type of sentence could be replied

![image]()




deployed by heroku :
------------------
--------------------------------------------------------
heroku container:push web --app joejoe2bot

heroku container:release web --app joejoe2bot

--------------------------------------------------------

deployed by aws elasticbeanstalk :
--------------------------------
--------------------------------------------------------
upload Dockerrun.aws.json(may need to modify port setting in Dockerfile)

and configure load balancer's port mapping and https

deployed by azure web app :
--------------------------------
--------------------------------------------------------
push image to docker hub

create a web app and specify using docker and set the image location
