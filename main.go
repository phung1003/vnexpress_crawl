package main

import (
	"fmt"
	"log"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type News struct {
	ID          int    `json:"id" gorm:"id"`
	Title       string `json:"title" gorm:"title"`
	Description string `json:"description" gorm:"description"`
	Image       string `json:"image" gorm:"image"`
	Link        string `json:"link" gorm:"link"`
}

func main() {
	dsn := "root:vttp1003@tcp(127.0.0.1:3306)/vnexpress"

	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})

	if err != nil {
		log.Fatalln(err.Error())
	}

	fmt.Println(db)

	r := gin.Default()

	items := r.Group("/items")
	{
		items.GET("/:id", GetItem(db))
		items.GET("", GetListItem(db))
	}

	r.Run()
}

func GetItem(db *gorm.DB) func(c *gin.Context) {
	return func(c *gin.Context) {
		var data News

		id, err := strconv.Atoi(c.Param("id"))
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}
		if err := db.Table("news").Where("id = ?", id).First(&data).Error; err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}

		c.JSON(http.StatusOK, gin.H{

			"data": data,
		})
	}
}

func GetListItem(db *gorm.DB) func(c *gin.Context) {
	return func(c *gin.Context) {
		var data []News
		if err := db.Table("news").Find(&data).Error; err != nil {
			c.JSON(400, gin.H{
				"error": err.Error(),
			})
			return
		}

		c.JSON(200, gin.H{
			"data": data,
		})
	}
}
