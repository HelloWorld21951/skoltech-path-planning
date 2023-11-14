from queue import PriorityQueue

q = PriorityQueue()
q.put("KEK")
q.put("LOL")
print(q.qsize())
q.get()
print(q.qsize())
q.get()
print(q.qsize())
