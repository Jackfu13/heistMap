
import requests
import json
from collections import defaultdict
import heapq

def findPaths(data):

    targets = set(data["targetSensors"])
    adj,roots = initGraph(data["sensors"],data["risks"])
    paths = []
    while targets:
        t,parent= dijkstra(adj,roots,targets)
        curPath = reconstructPath(parent,t)
        
        paths.append(curPath)
        zeroPaths(adj,curPath)
        targets.remove(t)
        
    return {"paths":paths}

def dijkstra(adj,roots,targets):
    dist={}
    parent={}
    heap  = []
    for r in roots:
        dist[r] = 0
        parent[r] = None
        heapq.heappush(heap, (0, r)) 
    while heap:
        d,id = heapq.heappop(heap)
        if d != dist.get(id,float('inf')):
            continue
        if id in targets:
            return id,parent
        for u,risk in adj[id]:
            if risk+d<dist.get(u,float('inf')):
                dist[u] = risk+d
                parent[u] = id
                heapq.heappush(heap,(risk+d,u))
    return None,parent

def reconstructPath(parent,target):
    path = []
    cur  = target
    while cur is not None:
      
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def zeroPaths(adj,path):
    for i in range(len(path)-1):
        u,v = path[i],path[i+1]
        for edge in adj[u]:
            if edge[0]==v:
                edge[1]=0
                break

def initGraph(sensors,risks):
    risk_map = {(r['fromSensor'], r['toSensor']): r['risk'] 
                for r in risks}
    adj  = defaultdict(list)
    for sensor in sensors:
        id = sensor["id"]
        for dependant in sensor["dependencies"]:
            adj[dependant].append([id,risk_map[(dependant,id)]])
    roots = [s['id'] for s in sensors if not s['dependencies']]
    return adj,roots

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

    paths = findPaths(data)
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


