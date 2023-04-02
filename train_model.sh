#!/bin/bash


#   Instala y prepara el entorno para entrenar el modelo GNPassGAN y PassGAN

#   El script se ha probado sobre un docker con miniconda3 preinstalado:
#   % docker pull conda/miniconda3
#   % docker run -it --platform linux/x86_64 conda/miniconda3 /bin/bash
#   % docker cp ./GNPASSGAN 444813e136b5:/home


###  Crear entorno ### 

#	echo "Creando entorno passgan..."
#	conda create -n passgan python=3.8 -y
#	echo "Activando entorno"
#	conda activate passgan
#	echo "Instalar pip"
#	conda install pip -y
#	echo "Intalar requirements.txt"
#	pip install -r requirements.txt

### Train GNPassGAN ###
training_data='./data/train_rockyou.txt'
output_dir='./output/GNPassGAN_27-02-2023'
save_every=10000
n_iters=250000
python3 './models.py' --training-data $training_data  --output-dir $output_dir --iters $n_iters --model 'gnpassgan' --save-every $save_every


### Train PassGAN ###
output_dir='./output/PassGAN_27-02-2023'
python3 './models.py' --training-data $training_data  --output-dir $output_dir --iters $n_iters --model 'passgan' --save-every $save_every



### Generate Passwords ###
model_trained_dir_vec=('./output/GNPassGAN_27-02-2023' './output/PassGAN_27-02-2023')
n_passwords=10 ** 8

n_trained_iters_vec=(10000 25000 50000 75000 100000 125000 150000 175000 200000 250000) #solo puedes coger de las que tengas entrenamiento
#n_trained_iters_vec=(10) #solo puedes coger de las que tengas entrenamiento

for model_trained_dir in "${model_trained_dir_vec[@]}"
do
    for n_trained_iters in "${n_trained_iters_vec[@]}"
    do
        #Run GENERATOR
        generated_passwords="${model_trained_dir}/evaluacion/generated_GNPassGAN_train${n_trained_iters}_len${n_passwords}.txt"
        echo "Generando ${n_passwords} contraseñas para el modelo ${n_trained_iters}"
        python3 './sample.py' --input-dir $model_trained_dir --output $generated_passwords --num-samples $n_passwords --training-iters $n_trained_iters

    done
done 