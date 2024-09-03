FROM golang:1.19-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
COPY . .
RUN go build -o main .

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=build /app/main .
EXPOSE 8080
CMD ["./main"]
