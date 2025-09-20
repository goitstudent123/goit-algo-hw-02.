from shared import LinkedList, merge_sorted

def main():
    ll = LinkedList([7, 3, 9, 1, 5])
    print("Initial:", ll.to_list())

    ll.reverse()
    print("Reversed:", ll.to_list())

    ll.insertion_sort()
    print("Sorted (insertion):", ll.to_list())

    a = LinkedList([1,3,5,7])
    b = LinkedList([2,4,6,8,10])
    merged_head = merge_sorted(a.head, b.head)
    merged = LinkedList()
    merged.head = merged_head
    print("Merged sorted lists:", merged.to_list())

    print("Conclusion: reverse changes links in-place; insertion_sort orders the list; merge_sorted combines two sorted lists preserving order.")

if __name__ == "__main__":
    main()
