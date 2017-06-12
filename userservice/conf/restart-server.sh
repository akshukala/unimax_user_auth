
sudo rm /etc/nginx/sites-enabled/default
sudo cp $PYTHONPATH/userservice/conf/userservice_nginx.conf /etc/nginx/sites-enabled/
pkill gunicorn
cd $PYTHONPATH/userservice/conf
echo $PWD
gunicorn -c gunicorn.py service_app:app
sudo service nginx restart


