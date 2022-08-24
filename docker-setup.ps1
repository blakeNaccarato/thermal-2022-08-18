$Name = Get-Location | Split-Path -Leaf
if ((docker volume inspect $Name) -eq '[]') { docker volume create $Name }
docker-compose up --build -d
