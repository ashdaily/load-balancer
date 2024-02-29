### Load balancer

#### This is a simple demonstration of a load balancer that runs locally and sits in front of four locally running http servers.

#### There are two files in the code base. 
- `python3 load_balancer.py` will run your loadbalancer on port 9000. 
- `python3 backend_servers.py` will run 4 backend_servers on port 8000, 8001, 8002, 8003.
- Make a simple curl request `curl -X GET http://127.0.0.1:9000` which returns hello world. 
- The request you send will be scheduled by the load balancer to the backend server in a roundrobin manner. 
- Each server returns the same response on the `/` path and GET method.
- This is a simple demonstration in python for how a round robin LoadBalancer can work in python3.

### Enjoy !