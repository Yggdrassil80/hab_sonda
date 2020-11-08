echo "*********************************************"
echo "HABCAT Herramienta de activación de servicios"
echo "*********************************************"

while read listaServicios; do

echo "Copiando archivo de servicios..."
for service in $listaServicios; do
    sudo cp /data/hab_sonda/services/$service.service /etc/systemd/system/$service.service
done
echo "Archivos copiados OK!"
echo "Reload del daemon de systemctl.."
sudo systemctl daemon-reload
echo "Recarga OK!"
echo "Activación de los servicios..."
for service in $listaServicios; do
    sudo systemctl enable $service.service
    sleep 2
done
echo "Todos los servicios activados!"
echo "Arranque de todos los servicios..."
for service in $listaServicios; do
    sudo systemctl start $service.service
    sleep 2
done
echo "Todos los servicios arrancados!"

done < /data/hab_sonda/utilities/services.conf
