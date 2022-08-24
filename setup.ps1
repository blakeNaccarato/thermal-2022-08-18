
$Name = "gunns-sims"

docker volume create --name $Name
docker build . -t $Name

$Volume = "\\wsl$\docker-desktop-data\data\docker\volumes\$Name\_data"
if ( !(Test-Path $Volume/.git) ) { git clone . $Volume }

docker run -id -v $Name:/root/$Name --name $Name $Name
