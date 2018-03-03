package main

import (
	"fmt"
	"net"
	"sync"
)

type Server struct {
	Port      string
	CurrentID int
	*sync.Mutex
}

type Client struct {
	connection *net.Conn
	id         int
}

func newClient(S *Server, C *net.Conn) *Client {
	client := Client{}
	S.Lock()
	defer S.Unlock()
	client.connection = C
	S.CurrentID++
	client.id = S.CurrentID
	return &client
}

func main() {
	server := Server{"18723", 0, &sync.Mutex{}}
	listener, err := net.Listen("tcp", "127.0.0.1:"+server.Port)

	if err != nil {
		panic(err)
	}
	defer listener.Close()
	defer (func() {
		fmt.Println("Closing....")
	})()

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err.Error())
			continue
		}

		go newClient(&server, &conn)
	}

}
