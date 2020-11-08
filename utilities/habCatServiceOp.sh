echo "****************************************************************"
echo "HABCAT Herramienta de gestion de servicios (start, stop, status)"
echo "****************************************************************"

while read listaServicios; do 

echo "Gestionando servicios..."
for service in $listaServicios; do
    sudo systemctl $1 $service.service
done
echo "Servicios Gestionados"

done < /data/hab_sonda/utilities/services.conf
