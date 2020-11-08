echo "************************************************"
echo "HABCAT Herramienta de desactivación de servicios"
echo "************************************************"

while read listaServicios; do

echo "Parada de los servicios..."
for service in $listaServicios; do
    sudo systemctl stop $service.service
    sleep 2
done
echo "Todos los servicios parados!"


echo "Desactivación de los servicios..."
for service in $listaServicios; do
    sudo systemctl disable $service.service
    sleep 2
done
echo "Todos los servicios desactivados!"

done < /data/hab_sonda/utilities/services.conf
