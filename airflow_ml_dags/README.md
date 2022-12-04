1. команда генерации образов и запуска контейнеров airflow из папки airflow_ml_dags  
docker compose up --build
   
2. команда для остановки airflow  
docker compose down
   
3. для будущих поколений, если при создании образа airflow-docker возникает ошибка  
strconv.Atoi: parsing "": invalid syntax  
   мне помогла команда  
   docker-compose down --remove-orphans
   
но лучше про нее почитать и применять с осторожностью
