echo "################################################################################################"
echo "                                  G19 - Kubernetes Deployment                                   "
echo "################################################################################################"

echo "\n\n[K8s] Deployment ###########################################################################"
echo "\n[K8s] Select Action to Execute"

items=( "Deploy" "Remove" )
select item in "${items[@]}" Quit
do
  read -p "[K8s] Do you Wish to $item Configuration? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

  case $REPLY in
    1)
      echo "\n[K8s] Starting Deployment from '.deployment'"
      kubectl apply -f ./deployment
      echo "\n[K8s] Finished Deployment from '.deployment'\n"
      break;;

    2)
      echo "\n[K8s] Starting Remove Deployment"
      kubectl delete ingress gateway-ingress-k8
      kubectl delete all --all -n default
      echo "\n[K8s] Finished Removing Deployment\n"
      break;;

    3)
      echo "\n[K8s] Quitting process\n"
      break;;

    *)
      echo "\n[K8s] Invalid Option. Exiting\n"
      break;;

  esac
done

echo "################################################################################################"
echo "                                      Completed Deployment                                      "
echo "################################################################################################"
exit 0