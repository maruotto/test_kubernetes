# Deploying microservices Using Kubernetes
## Usage
To deploy a cluster and simulate cloud architecture, this application uses minikube. 
It creates a cluster with one slave node. All pods will 
be spawned in it.

 ```sh
minikube start
```
Tunnel, o allow external connection to the cluster and 
expose the cluster itself using its external ip.
This command requires sudo (or administrator priviledges)
because it will open port<1024. [port 80 in this case]
Necessary only if using an ingress.
 ```sh
minikube tunnel
```

Spawn the deployments

_use ```minikube kubectl -- args``` instead of ```kubectl args``` if 
minikube is not set as default kubernetes cluster, or set it_
 
```sh
 kubectl apply -f deployments.yml
```

Spawn the services (one for each deployment)
```sh
 kubectl apply -f service.yml
```

### Connecting to the services
Spawn the ingress (one for all the services).
The ingress will create a single entrypoint for 
all the services. Moreover, it can be associated to a 
registered domain, and some paths in it.
```sh
 kubectl apply -f service.yml
```
 OR

Do manual port forwarding for each service (example for 
patient 540).
```sh
kubectl port-forward svc/svc-540-service 5400:8081
```

## How to create images used in deployment

Having saved tensorflow models (not in h5 format), 
these are the steps (described for patient 540 and 
replicated for all of them):

- Run daemon docker container using _tensorflow/serving_ as image 
and associate a name to this container.
 ```shell
docker run -d --name serving_540 tensorflow/serving
```

- copy model folder in the container, in the correct folder
 ```shell
docker cp /path/to/model/540 serving_540:/models/540
```
- change model name environment variable value to the correct one 
(this name will be used later to do inference)
```shell
docker commit --change "ENV MODEL_NAME 540" serving_540 540
```

- kill the daemon
```shell
docker kill serving_540
```

### Docker hub publication
- tag the image to a repository
```shell
docker tag serving_540:latest utente/540:latest 
```

- push to the previously created repository
```sh
docker push nanigo/nome_repository:latest
```

