package main


import (
    "fmt"
)

type TrueNode struct {
	txt string
	yes *TrueNode
	no *TrueNode
}

type Node struct {
	TrueHead *TrueNode
}

func main() {

}

