#!/bin/bash

model_trained_dir_vec=('./output/GNPassGAN_27-02-2023' './output/PassGAN_27-02-2023')
n_passwords=500

#n_trained_iters_vec=(10000 50000 100000 150000 200000) #solo puedes coger de las que tengas entrenamiento
n_trained_iters_vec=(10) #solo puedes coger de las que tengas entrenamiento

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