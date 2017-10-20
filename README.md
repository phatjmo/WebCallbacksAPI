Get Leads from ICAP:

`curl -u optimise:end2endComm -vX GET http://localhost:4295/api/v1.0/webcallbacks/ICAP`

Post Leads to ICAP:

`curl -u optimise:end2endComm -vX POST http://localhost:4295/api/v1.0/webcallbacks/ICAP -d @test.json --header "Content-Type: application/json"`

Delete Leads from ICAP:

`curl -u optimise:end2endComm -vX DELETE http://localhost:4295/api/v1.0/webcallbacks/ICAP`

Use docker host IP and port 80 in URL if you are building from docker-compose.