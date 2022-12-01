# artem_denisov
запускать из корневого каталога репозитория

1. команда для сборки образа Docker  
sudo docker build sibarin/online_inference:v1
   

2. команда для запуска контейнера Docker  
   docker run -p 8000:8000 sibarin/online_inference:v1
   

3. команда для пуша образа в Docker hub  
docker push sibarin/online_inference:v1  
   
   
4. команда для пулла образа из Docker hub  
docker pull sibarin/online_inference:v1
