from sklearn.metrics.pairwise import cosine_similarity
# import heapq
# def heapq_int():
#     heap = []
#     #以堆的形式插入堆
#     heapq.heappush(heap,10)
#     heapq.heappush(heap,1)
#     heapq.heappush(heap,10/2)
#     heapq.heappush(heap, 2)
#     heapq.heappush(heap, 15)
#     heapq.heappush(heap, 4)
#     heapq.heappush(heap, 0.5)
#     print(heap)
#
#
# heapq_int()

print(cosine_similarity([[1,3,2],[2,2,1]])[0][1])

list = [1, 2, 3, 4, 5, 5, 6, 7]
print(list)
list.pop(-3)
print(list)
