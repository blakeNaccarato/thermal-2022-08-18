$Name = Get-Location | Split-Path -Leaf
if ((docker volume inspect $Name) -eq '[]') {
    docker volume create $Name
}
else {
    docker volume rm $Name
}
docker-compose up --build -d
