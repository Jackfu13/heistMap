from collections import defaultdict
import heapq
import requests
import json

def find_paths(data):
    adj, roots,edges = build_graph(data["sensors"],data["risks"])
    targets = set(data["targetSensors"])
    
    paths = []
    while targets:
        parent,target = dijkstra(adj,roots,targets)
       
        targets.remove(target)
        path = reconstruct_path(parent,target)
       
        zero_edges(path,edges)
        paths.append(path)
    return {"paths":paths}
def zero_edges(path,edges):
    for i in range(len(path)-1):
        u,v = path[i],path[i+1]
        edges[(u,v)][1] = 0
def reconstruct_path(parent,target):
    curr = target
    path = []
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path
def dijkstra(adj,roots,targets):
    dist = {}
    parent = {}
    heap = []
    for root in roots:
        dist[root] = 0
        parent[root] = None
        heapq.heappush(heap,(0,root))
    
    while heap:
        d,curr = heapq.heappop(heap)
        if d > dist.get(curr,float("inf")):
            continue
        if curr in targets:
            return parent,curr
        for v,w in adj[curr]:
            if d+w < dist.get(v,float("inf")):
                dist[v] = d+w
                parent[v] = curr
                heapq.heappush(heap,(d+w,v))
    return parent,None

def build_graph(sensors,risks):
    riskmap = {(s["fromSensor"],s["toSensor"]): s["risk"]
               for s in risks}
    roots = [s["id"] for s in sensors if not s["dependencies"]]
    adj  = defaultdict(list)
    edges = {}
    for sensor in sensors:
        for dependant in sensor["dependencies"]:
            pair = [sensor["id"],riskmap[(dependant,sensor["id"])]]
            adj[dependant].append(pair)
            edges[(dependant,sensor["id"])] = pair
    return adj,roots,edges


def main():
    id = "990ac0bb-63e1-4180-9ea3-864983cedaa9"

    response  = requests.get(
    f"https://challenge.generatenu.com/api/v1/challenge/algorithm/{id}"
    )
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error:", response.status_code, response.text)
        exit()
    paths = find_paths(data)
    answer = requests.post(
    f"https://challenge.generatenu.com/api/v1/challenge/algorithm/{id}/submit",
    headers={
      "Content-Type": "application/json"
    },
    json=paths
)
    print("Status:", answer.status_code)
    print(answer.text)
if __name__=="__main__":
    main()

