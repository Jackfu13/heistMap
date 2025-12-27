
import requests
import json
from collections import defaultdict
import heapq
def find_paths(data):
    targets = set(data["targetSensors"])
    adj,roots,edges = initGraph(data["sensors"],data["risks"])
    paths = []
    while targets:
        t,parent= dijkstra(adj,roots,targets)
        if t is None:
            break
        curPath = reconstructPath(parent,t)
        paths.append(curPath)
        zeroPaths(curPath,edges)
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
        if d > dist.get(id,float('inf')):
            continue
        if id in targets:
            return id,parent
        for u,risk in adj[id]:

            newDist = risk+d
            oldDist = dist.get(u, float('inf'))
            if (newDist < oldDist) :
                dist[u] = newDist
                parent[u] = id
                heapq.heappush(heap, (newDist, u))
    return None,parent
def reconstructPath(parent,target):
    path = []
    cur  = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path
def zeroPaths(path,edges):
    for i in range(len(path)-1):
        u,v = path[i],path[i+1]
        edge = edges[(u,v)]
        edge[1]=0
def initGraph(sensors,risks):
    risk_map = {(r['fromSensor'], r['toSensor']): r['risk'] 
                for r in risks}
    adj  = defaultdict(list)
    edges = {}
    for sensor in sensors:
        id = sensor["id"]
        for dependant in sensor["dependencies"]:
            edge = [id,risk_map[(dependant,id)]]
            edges[(dependant,id)] = edge
            adj[dependant].append(edge)
    roots = [s['id'] for s in sensors if not s['dependencies']]
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


