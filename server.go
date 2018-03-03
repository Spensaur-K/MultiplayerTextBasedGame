package main

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"
	"strings"
	"time"
)

type Server struct {
	Port      string
	CurrentID int
}

type Client struct {
	connection *net.Conn
	id         int
}

func newClient(S *Server, C *net.Conn) *Client {
	client := Client{}
	client.connection = C
	S.CurrentID++
	client.id = S.CurrentID
	return &client
}

func handleClient(nc *Client) {

	cmd := exec.Command("rw.py")
	fmt.Fprintln(cmd.Stdout, "Hello World, This is Tobias! & Evan")
	data, _ := cmd.Output()
	fmt.Println(string(data))
}

func garbage() {
	cmd := exec.Command("python3", "rw.py")
	cmd.Stdin = strings.NewReader("some input")
	var out bytes.Buffer
	cmd.Stdout = &out

	err := cmd.Start()

	if err != nil {
		panic(err)
	}
	time.Sleep(time.Second)
	fmt.Printf("stuff %q\n", out.String())
}

func main() {
	garbage()
	server := Server{"18723", 0}
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
		nc := newClient(&server, &conn)
		go handleClient(nc)
	}

}
