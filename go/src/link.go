package main

import "fmt"

type Node struct {
	data int
	next *Node
}

func Append(x int) *Node {
	r := Node{data:x, next:nil}
	return &r
}

func buildLink(x int) *Node {
	h := &Node{}
	r := h
	for i:=1; i<x;i++{
		h.next = Append(i)
		h = h.next
	}
	fmt.Println(r)
	return r
}

func length(h *Node) int {
	i := 1
	for h.next != nil{
		i++
		h = h.next
		fmt.Println(h.data)
	}
	return i
}


func main()  {
	r := buildLink(10)
	fmt.Println(length(r))

}