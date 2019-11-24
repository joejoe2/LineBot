# LineBot

app https://joejoe2bot.herokuapp.com
 
line reply post endpoint  https://joejoe2bot.herokuapp.com/callback
   

depoly by heroku :
------------------
--------------------------------------------------------
heroku container:push web --app joejoe2bot

heroku container:release web --app joejoe2bot

--------------------------------------------------------

deploy by aws elasticbeanstalk :
--------------------------------
--------------------------------------------------------
upload Dockerrun.aws.json(may need to modify port setting in Dockerfile)

and configure load balancer's port mapping and https

deploy by azure web app :
--------------------------------
--------------------------------------------------------
push image to docker hub

create a web app and specify using docker and set the image location
