#!/bin/sh

for ARGUMENT in "$@"
do
   KEY=$(echo $ARGUMENT | cut -f1 -d=)

   KEY_LENGTH=${#KEY}
   VALUE="${ARGUMENT:$KEY_LENGTH+1}"

   export "$KEY"="$VALUE"
done

frontend(){
   echo "Running frontend $framework"
   if [[ $framework == "react" ]]
   then
      cd client && export PORT=3001 && npm start
   fi
   if [[ $framework == "dash" ]]
   then
      python run_dash_frontend.py $yaml
   fi
}

server(){
    echo "Running $yaml"
    is_elastic=$(echo $(python3.9 parse_yaml.py $yaml models_search)| grep -c "ElasticBERT")
    is_webexBot=$(echo $(python3.9 parse_yaml.py $yaml UI)| grep -c "webex_bot")
    is_slackBot=$(echo $(python3.9 parse_yaml.py $yaml UI)| grep -c "slack_bot") 
    if (($is_elastic >= 1 ))
    then
		is_elastic_service_running=$(echo $(curl http://localhost:9200/_cluster/health) | grep -c "elasticsearch")
      # echo $is_elastic_service_running
      if (($is_elastic_service_running < 1))
      then
         echo -e "\n\n\nTrying to run elastic seach\n\n\n\n\n"
         bash ../elasticsearch/bin/elasticsearch
         sleep 10
         is_elastic_service_running=$(echo $(curl http://localhost:9200/_cluster/health) | grep -c "elasticsearch")
         if (($is_elastic_service_running < 1))
         then
            echo -e "\n\n\n\nPlease Run Elastic Search to run the backend\n\n\n\n"
         else
            python run_backend.py $yaml & disown
         fi
      else
         python run_backend.py $yaml & disown
      fi
    else
      python run_backend.py $yaml & disown
	 fi
    if (($is_webexBot >= 1 ))
    then
      sleep 10
      python external_apps/webex_bot/main.py 
    fi
    if (($is_slackBot >= 1 ))
    then
      sleep 10
      python external_apps/slack_bot/run.py 
    fi    
}

echo $1
case $1 in

  "build")
	 echo "Building local development environment"
	 curl https://pyenv.run | bash
	 pyenv install -v 3.9.16
	 pyenv virtualenv 3.9.16 venv
	 pyenv activate venv
    ;;

   "install")
    echo "Installing dependencies"
	 pip install -r requirements.txt
	 cd client && npm install
    ;;

  "frontend")
    frontend
	 ;;	

  "server")
    server
    ;;
   
  "bot")
    python external_apps/webex_bot/main.py   
  ;; 

  *)
    server &
    P1=$!
    frontend &
    P2=$!
    wait $P1 $P2
    ;;
esac