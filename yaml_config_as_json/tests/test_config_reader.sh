export SERVICEREPO=immersa-co/api
export CONFIGREF=main
export TENANTNAME=dev01
export GHATOKEN="$(python3 ~/utils/generateGithubAppToken.py)"

#python3 ../main.py

../config_reader.sh
