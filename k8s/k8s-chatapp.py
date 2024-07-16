----------------------------------Dockerfile------------------------------------------
# Use the official PHP image as a base image
FROM php:apache

# Copy the contents of the current directory into the /var/www/html directory in the container
COPY . /var/www/html/

# Install mysqli extension
RUN docker-php-ext-install mysqli

# Set index.php as the default index file
RUN echo "DirectoryIndex index.php" >> /etc/apache2/apache2.conf

# Expose port 80
EXPOSE 80



---------------------------------Docker-compose.yaml----------------------------------
version: '3.8'

services:
  web:
    build: .
    container_name: chat_app_web
    ports:
      - "8080:80"
    networks:
      - chat-app-network
    depends_on:
      - mysql

  mysql:
    image: mysql:5.7
    container_name: chat_app_mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: chatapp
      MYSQL_USER: chatuser
      MYSQL_PASSWORD: chatpassword
    volumes:
      - db_data:/var/lib/mysql
    networks:
      - chat-app-network

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: chat_app_phpmyadmin
    environment:
      PMA_HOST: mysql
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "8081:80"
    networks:
      - chat-app-network

volumes:
  db_data:

networks:
  chat-app-network:
    driver: bridge


---------------------------------Docker-compose file management-----------------------
@step: 01 Manage container
Start containers: docker-compose up -d
Stop containers: docker-compose down
View logs: docker-compose logs -f
List containers: docker ps

@step: 02 Incase of issue
docker-compose down
docker-compose up --build -d

@@@@@step: xx   CLEAN ALL DOCKER IMAGES
docker system prune -a --volumes


@step: 02 Access the application
http://localhost:8080  ---> application endpoint
http://localhost:8081  ---> phpmyadmin endpoint


@or just build image with docker-compose
docker-compose build
docker images


---------------------------------Push docker image to dockerhub.io-----------------------

@step 01: tag docker image with docker username
docker tag chat-app_web:latest fattah2024/chat-app-web:1.0.0

@step 02: login into docker.io (if not logged in yet)
docker login

@step 03: push the docker image into repo
docker push fattah2024/chat-app-web


-------------------------------------------minikube--------------------------------------
@step: 01 start minikube
minikube start
minikube status

@step: 02 delete everything for a fresh start
kubectl delete --all pods --all-namespaces
kubectl delete --all services --all-namespaces
kubectl delete --all deployments --all-namespaces
kubectl delete --all statefulsets --all-namespaces
kubectl delete --all daemonsets --all-namespaces
kubectl delete --all replicasets --all-namespaces
kubectl delete --all jobs --all-namespaces
kubectl delete --all cronjobs --all-namespaces


@step: 03 create alias for kubectl
alias k="kubectl"


@step: 04 create web-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app-web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chat-app-web
  template:
    metadata:
      labels:
        app: chat-app-web
    spec:
      containers:
      - name: chat-app-web
        image: fattah2024/chat-app-web:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: chat-app-web
spec:
  type: NodePort
  selector:
    app: chat-app-web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080




@step: 05 create mysql-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app-mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chat-app-mysql
  template:
    metadata:
      labels:
        app: chat-app-mysql
    spec:
      containers:
      - name: chat-app-mysql
        image: mysql:5.7
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: rootpassword
        - name: MYSQL_DATABASE
          value: chatapp
        - name: MYSQL_USER
          value: chatuser
        - name: MYSQL_PASSWORD
          value: chatpassword
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
---
apiVersion: v1
kind: Service
metadata:
  name: chat-app-mysql
spec:
  ports:
    - port: 3306
  selector:
    app: chat-app-mysql


@step: 06 create phpmyadmin-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app-phpmyadmin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chat-app-phpmyadmin
  template:
    metadata:
      labels:
        app: chat-app-phpmyadmin
    spec:
      containers:
      - name: chat-app-phpmyadmin
        image: phpmyadmin/phpmyadmin
        env:
        - name: PMA_HOST
          value: chat-app-mysql
        - name: MYSQL_ROOT_PASSWORD
          value: rootpassword
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: chat-app-phpmyadmin
spec:
  type: NodePort
  selector:
    app: chat-app-phpmyadmin
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30081


@step: 08
kubectl apply -f mysql-pv.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f web-deployment.yaml
kubectl apply -f phpmyadmin-deployment.yaml


@step: 09 get minikube ip
minikube ip

@step 09: get deployment status
k get deployments
k describe deployment chat-app-web-public

k get pods
k get service

-----------------------------------------Access to chat-app----------------------------------
@step: 01 Access to deployment

Web Application: http://<minikube-ip>:30080
phpMyAdmin: http://<minikube-ip>:30081


@Note:
MySQL Database Credentials
Hostname: chat-app-mysql
Username: chatuser
Password: chatpassword
Database: chatapp
These credentials are configured in your MySQL deployment (mysql-deployment.yaml).

phpMyAdmin Credentials
URL: http://192.168.49.2:30081/
Username: root
Password: rootpassword
These credentials are configured in your phpMyAdmin deployment (phpmyadmin-deployment.yaml).

Application Access (assuming your application URL)
Web Application URL: http://192.168.49.2:30080



-------------------------------------Scale Up/Down-------------------------------------------
@step: 01 get deployments which one needs to scale up or down
kubectl get deployments

@step: 02 using kubectl scale cmd
kubectl scale deployment <your-deployment-name> --replicas=3

@check upscalling using cmd kubectl get pods
NAME                                   READY   STATUS              RESTARTS      AGE
chat-app-mysql-779c84d999-272nf        1/1     Running             1 (11h ago)   12h
chat-app-phpmyadmin-7676bbbfb5-2n76n   1/1     Running             1 (11h ago)   12h
chat-app-web-74f6659876-2jhqq          1/1     Running             0             3s
chat-app-web-74f6659876-csbl4          0/1     ContainerCreating   0             3s
chat-app-web-74f6659876-gnwg9          1/1     Running             1 (11h ago)   12h

@step: 03 Scale down using the same command
kubectl scale deployment <your-deployment-name> --replicas=1
@check scalling down
kubectl get pods
NAME                                   READY   STATUS        RESTARTS      AGE
chat-app-mysql-779c84d999-272nf        1/1     Running       1 (12h ago)   12h
chat-app-phpmyadmin-7676bbbfb5-2n76n   1/1     Running       1 (12h ago)   12h
chat-app-web-74f6659876-2jhqq          0/1     Terminating   0             6m37s
chat-app-web-74f6659876-gnwg9          1/1     Running       1 (12h ago)   12h



---------------------------------------LoadBalancerIP------------------------------------------
@step: 01 update specs of web-deployment.yaml type to LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  name: chat-app-web
spec:
  type: LoadBalancer	#instead of NodePort
  selector:
    app: chat-app-web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080
      


@scaleup:
kubectl scale deployment <your-deployment-name> --replicas=1

@step: 02 Use minikube service cmd
k get svc
AME                  TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
chat-app-mysql        ClusterIP      10.102.220.33   <none>        3306/TCP       12h
chat-app-phpmyadmin   NodePort       10.109.220.11   <none>        80:30081/TCP   12h
chat-app-web          LoadBalancer   10.109.61.254   <pending>     80:30080/TCP   12h
kubernetes            ClusterIP      10.96.0.1       <none>        443/TCP        12h

minikube service chat-app-web  ----> this one will open browser with random pods response by LoadBalancer.


@step: 03 Get details of each spinned up pods with their ip 
kubectl get pods -l app=chat-app-web -o wide

NAME                            READY   STATUS    RESTARTS      AGE     IP            NODE       NOMINATED NODE   READINESS GATES
chat-app-web-74f6659876-5gkhx   1/1     Running   0             3m58s   10.244.0.16   minikube   <none>           <none>
chat-app-web-74f6659876-gnwg9   1/1     Running   1 (12h ago)   12h     10.244.0.11   minikube   <none>           <none>
chat-app-web-74f6659876-txv82   1/1     Running   0             3m58s   10.244.0.15   minikube   <none>           <none>


@step: 04 Get access to specific pods using port forward cmd
Base cmd: kubectl port-forward pod/chat-app-web-<pod-id> 8080:80
example: kubectl port-forward pod/chat-app-web-74f6659876-5gkhx 8080:80

@step: 05 access it from another terminal to that specific pod
curl http://localhost:8080




---------------------------------------Namespace--------------------------------------------
info: Add namespace to the deployment to isolate the production and Shaddow environment
(Need to be added both in deployment and service section like this)


apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-app-web
  namespace: production   # Specify the namespace here
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chat-app-web
  template:
    metadata:
      labels:
        app: chat-app-web
    spec:
      containers:
      - name: chat-app-web
        image: fattah2024/chat-app-web:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: chat-app-web
  namespace: production   # Specify the namespace here
spec:
  type: NodePort
  selector:
    app: chat-app-web
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080


@step: 01: Create namespaces as needed
kubectl create namespace production
kubectl create namespace shadow

@step: 02 update all the deployment and service yamls and then apply in minikube
k apply -f mysql-pv.yaml -n production
k apply -f web-deployment.yaml -n production
k apply -f mysql-deployment.yaml -n production
k apply -f phpmyadmin-deployment.yaml -n production
--------------or----------------------------
k apply -f mysql-pv.yaml -n shadow
k apply -f web-deployment.yaml -n shadow
k apply -f mysql-deployment.yaml -n shadow
k apply -f phpmyadmin-deployment.yaml -n shadow



@step: 03 get all the namespaces
kubectl get namespaces -o wide

@delete namespaces
kubectl delete namespace production
kubectl delete namespace shadow



@step: 04 get all the pods for specific namespace
kubectl get pods -n production
kubectl get svc -n production
kubectl get deployments -n production


@step: 05 run the deployment
minikube service chat-app-web -n production
minikube service chat-app-web -n shadow


@step: 02 delete everything for a fresh start
kubectl delete --all pods --all-namespaces
kubectl delete --all services --all-namespaces
kubectl delete --all deployments --all-namespaces
kubectl delete --all statefulsets --all-namespaces
kubectl delete --all daemonsets --all-namespaces
kubectl delete --all replicasets --all-namespaces
kubectl delete --all jobs --all-namespaces
kubectl delete --all cronjobs --all-namespaces


@@@@@step: xx   CLEAN ALL DOCKER IMAGES
docker system prune -a --volumes






-----------------------------------GCP Kubernetes-------------------------------
@step: 01 Open GCP console and create new project

@step: 02 Activate Kubernetes Engine API

@step: 03 GO to kubernetes cluster and create using standard cluster































































