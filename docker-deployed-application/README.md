## Usage
Build docker image
 ```sh
docker build --tag glucose-prediction . 
```
Run docker image
 ```sh
docker run --publish 8501:8501 --name=glucose-prediction-web-app --net=minikube glucose-prediction
```
To make the app work, it is mandatory to connect it to the
microservices, these can be accessible through bridge connection. 

In particular, the container is connected to minikube network. 
On the same network is connected kubernetes cluster.