$Name = "gunns-sims_volume"
docker volume create --name $Name
$Volume = "\\wsl$\docker-desktop-data\data\docker\volumes\$Name\_data"
if ( !(Test-Path $Volume/.git) ) { git clone . $Volume }
docker-compose up -d
