# dockerize.py
# This file should be exactly what you produce after
# you finish the accompaning tutorial.
# (Make sure to change the repository directory in line 12)

from docker import from_env 
import os 

client = from_env()

# get paths
repo_dir = os.path.join('/absolute/path/to/tutorial', 'django-todo')
web_pth = os.path.join(repo_dir, 'web')
api_pth = os.path.join(repo_dir, 'api')
# build images
web_img, logs = client.images.build(path=web_pth, tag='web')
api_img, logs = client.images.build(path=api_pth, tag='api')

net_name = 'djang-net'
net = client.networks.create(name=net_name, driver='bridge')

# ports  
api_ports  =  {'8000/tcp'  :  8000}  
web_ports  =  {'8080/tcp'  :  8080}  
web_env  =  ["HOST=0.0.0.0"]  

# volumes  
api_vol  =  {  
	os.path.join(repo_dir,  'api/django_todo') : { 'bind':  '/usr/src/app',  'mode':  'rw'} 
	}  
web_vol  =  {  
	os.path.join(repo_dir,  'web/vue-todo')  :  {  'bind'  :  '/usr/src/app',  'mode'  :  'rw'}  
	}  
db_vol  =  {  
	os.path.join(repo_dir,  'dbdata')  :  {'bind'  :  '/var/lib/postgresql/data'} 
	}

# launch

db = client.containers.run('postgres:10', detach=True, name='db', 
                           network=net_name, volumes=db_vol)

api = client.containers.run(api_img, ports=api_ports, detach=True, 
                            name='api', network=net_name, volumes=api_vol,
                            command="sh back.sh")
                            
web = client.containers.run(web_img, ports=web_ports, detach=True,
                           name='web', network=net_name, volumes=web_vol,
                           environment=web_env, command="sh front.sh")
