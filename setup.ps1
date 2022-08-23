$Volume = '\\wsl$\docker-desktop-data\data\docker\volumes\gunns-sims_volume\_data'
if ( !(Test-Path $Volume/.git) ) { git clone . $Volume }
docker-compose up -d
