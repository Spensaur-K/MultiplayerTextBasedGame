package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"os/exec"
)

type Game struct {
	gameInChannel  chan string
	gameOutChannel chan string
}

type Server struct {
	Port      string
	CurrentID int
}

type Client struct {
	connection net.Conn
	id         int
}

func newClient(S *Server, C net.Conn) *Client {
	client := Client{}
	client.connection = C
	S.CurrentID++
	client.id = S.CurrentID
	return &client
}

func handleClient(nc *Client, game Game) {
	var fromClientData []byte
	var err error

	reader := bufio.NewReader(nc.connection)

	go func() {
		for err == nil {
			fromClientData, _, err = reader.ReadLine()
			game.gameInChannel <- string(fromClientData)
		}
		nc.connection.Close()
	}()

	var writeErr error
	go func() {
		for writeErr == nil {
			data := <-game.gameOutChannel
			nc.connection.Write([]byte(data))
		}
		nc.connection.Close()

	}()

}

func producer(gameIn io.WriteCloser, inChannel chan string) {
	var err error

	go func() {
		for err == nil {
			fmt.Fprintln(gameIn, <-inChannel)

		}
		if err != nil {
			panic(err)
		}
	}()
}

func consumer(reader *bufio.Reader, outChannel chan string) {
	var data []byte
	var err error

	go func() {
		for err == nil {
			data, _, err = reader.ReadLine()
			outChannel <- string(data)

		}
		if err != nil {
			panic(err)
		}
	}()
}

//todo
func handleClientWrites(connectionMap map[int]*Client, game Game) {

}

func bindStdInAndStdOut(name string, arg ...string) (io.WriteCloser, *bufio.Reader) {
	cmd := exec.Command(name, arg...)

	pipeIn, err := cmd.StdinPipe()
	if err != nil {
		panic(err)
	}

	pipeOut, err := cmd.StdoutPipe()
	if err != nil {
		panic(err)
	}

	readerOut := bufio.NewReader(pipeOut)
	cmd.Start()

	return pipeIn, readerOut

}

func main() {

	gameIn, gameOut := bindStdInAndStdOut("python3", "rw.py")
	gameInChannel := make(chan string)
	gameOutChannel := make(chan string)
	producer(gameIn, gameInChannel)
	consumer(gameOut, gameOutChannel)

	game := Game{gameInChannel, gameOutChannel}
	connectionMap := make(map[int]*Client)
	handleClientWrites(connectionMap, game)
	port := "18723"
	fmt.Print("Listening on port: ", port)
	server := Server{port, 0}
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
		nc := newClient(&server, conn)
		connectionMap[nc.id] = nc

		go handleClient(nc, game)
	}
}
