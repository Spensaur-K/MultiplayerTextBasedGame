package main

import (
	"bufio"
	"fmt"
	"net"
	"os/exec"
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

func readPy(cmd *exec.Cmd) {
	pipeOut, err := cmd.StdoutPipe()
	if err != nil {
		panic(err)
	}

	reader := bufio.NewReader(pipeOut)
	var data []byte

	go func() {
		for err == nil {
			data, _, err = reader.ReadLine()
			fmt.Printf("stuff: %s\n", string(data))
		}
	}()
}

func garbage() {
	cmd := exec.Command("python3", "rw.py")

	pipeIn, err := cmd.StdinPipe()
	if err != nil {
		panic(err)
	}

	readPy(cmd)
	cmd.Start()
	for x := 0; x < 100; x++ {
		fmt.Fprintln(pipeIn, x)
	}

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
