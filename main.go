package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"time"
)

// Sets necessary parameters for program to run
const addonDir, downloadDir, apiUrl, sourceUrl string = "C:/Program Files (x86)/World of Warcraft/_retail_/Interface/Addons", "C:/Users/kbh78/Downloads", "https://api.github.com/repos/tukui-org/ElvUI/branches/main", "https://github.com/tukui-org/ElvUI/archive/refs/heads/main.zip"

func main() {
	start := time.Now()
	// fmt.Println("Hello, World!")
	getVersionNumber()
	getZipFileName()
	checkLocalVersion()
	end := time.Now()
	fmt.Printf("Completed in %v\n", end.Sub(start))
}

type Todo struct {
	Name   string `json:"name"`
	Commit struct {
		Commit struct {
			Message string `json:"message"`
		}
	}
}

func getVersionNumber() string {
	resp, err := http.Get(apiUrl)
	if err != nil {
		log.Fatalln(err)
	}
	defer resp.Body.Close()
	bodyBytes, _ := ioutil.ReadAll(resp.Body)
	// Convert response body to Todo struct
	// var todoStruct Todo
	todoStruct := Todo{}
	jsonErr := json.Unmarshal(bodyBytes, &todoStruct)
	if jsonErr != nil {
		log.Fatal(jsonErr)
	}
	message := todoStruct.Commit.Commit.Message
	return message
}

func getZipFileName() string {
	urlSplitList := strings.Split(apiUrl, "/")
	zipFileName := urlSplitList[5] + "-" + urlSplitList[7]
	return zipFileName
}

func checkLocalVersion() {
	zipFileName := getZipFileName()
	versionNumber := getVersionNumber()
	downloadDirList, err := os.ReadDir(downloadDir)
	if err != nil {
		log.Fatal(err)
	}
	for _, entry := range downloadDirList {
		if entry.Name() == zipFileName+" "+versionNumber+".zip" {
			fmt.Println("Current version already exists in", downloadDir)
		}
	}
	return
}

func getSourceZipData() {}
func getZipFilePath()   {}
func manageZip()        {}
func managePaths()      {}
