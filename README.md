# LineBot


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
