# LineBot

app https://joejoe2bot.herokuapp.com
 
line reply post endpoint  https://joejoe2bot.herokuapp.com/callback
   
broadcast push endpoint  https://joejoe2bot.herokuapp.com/broadcast?data=[text_data]

push endpoint https://joejoe2bot.herokuapp.com/broadcast?id=[target_id]&data=[text_data]

remove [...] and fill your content


depoly by heroku :

--------------------------------------------------------
heroku container:push web --app joejoe2bot
heroku container:release web --app joejoe2bot


deploy by aws elasticbeanstalk :

--------------------------------------------------------
upload Dockerrun.aws.json
