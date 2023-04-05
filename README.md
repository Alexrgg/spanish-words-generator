# LenguageGAN

Este repositorio contiene la práctica final de texto de la asignatura datos no estructurados. en ella se ha implementado hoy un modelo de texto generativo mediante el uso de GANs con el objetivo de generar palabras nuevas de un idioma. 

Para ello se ha entrenado primero la GAN con el lenguaje español. Después, se han probado a generar palabras nuevas y midiendo cuantas de esas palabras nuevas se encuntran en el conjunto de test, es decir, son palabras qué verdaderamente existen.

El proyecto está basado en las implemntaciones de GNPassGAN y PassGAN con la implementación de [Gradient Normalization](https://github.com/basiclab/GNGAN-PyTorch) en Pytorch 1.10.

El modelo utilizado en PassGAN está inspirado en el artículo [Improved Training of Wasserstein GANs](https://arxiv.org/abs/1704.00028) y su versión pytorch [improved_wgan_training](https://github.com/caogang/wgan-gp).

## Instalar dependencias

```bash
# requiere que CUDA 10 esté preinstalado
python3 -m venv .venv 
source .venv/bin/activate  
pip3 install -r requirements.txt
```

## Dataset

Se ha usado como dataset para entrenar el modelo las palabras en español descargadas de https://github.com/JorgeDuenasLerin/diccionario-espanol-txt.

Como conjunto de test se ha usado una fuente distinta, los diccionarios descargados de https://github.com/titoBouzout/Dictionaries. Estos diccionarios de distintos idiomas se han tenido que preprocesar para prepararlos para usarlos en la evaluación del modelo. Este preprocesado se ha realizado con el netebook `preprocesar_dic.ipynb`.


## Código

El código para entrenar el modelo, generar las contraseñas y analizar el accuracy es `run_in_colab.ipynb`. En el se realizan las llamadas para realizar los siguientes pasos:

#### Entrenar el Modelo

```python
!python3 './models.py' --training-data '{training_data}'  --output-dir '{output_dir}' --iters '{n_iters}'`
```

#### Generar Contraseñas

```python
!python3 './sample.py' --input-dir '{model_trained_dir}' --output '{generated_passwords}' --num-samples '{n_passwords}' --training-iters '{n_trained_iters}'
```

#### Calcular Accuracy

```python
!python3 './accuracy.py' --input-generated '{generated_passwords_file}' --input-test '{training_file_path}' --n-passwords-vec {n_passwords_vec}
```


## Resultados

El codigo creado para analizar y generar las gráficas se encuentra en el notebook `read_logs.ipynb`.


### Análisis del Entrenamiento

En primer lugar, se pueden analizar la evolución de la función de perdidas tanto para el discriminante (la primera) como para el generador (la segunda). La función de perdidas usada es BCEWithLogitsLoss(), una función de entropía cruzada binaria. 

Dentro de las GAN, la función de pérdida se usa para medir la diferencia entre la probabilidad qué el discriminador asigna  a un conjunto de muestras reales y sintéticas de qué sean reales (en este caso en concreto). Es decir, si la salida del discriminador es 0.8 significará qué existe una probabilidad del 80% qué la palabra de entrada sea real. Si la palabra era verdaderamente real se calculará la diferencia de las probabilidades entre un 0.8 y un 1 (la salida esperada).

![train_critic_cost](./img/train_critic_cost.jpg)


![train_gen_cost](./img/train_gen_cost.jpg)

En la figura se puede observar cómo en las primeras iteraciones la función de costes tanto para el discriminador como para el generador oscila entre 1.2 y 0.8. A medida que se suceden las iteraciones la función de costes del discrimínate tiende a crecer y la del generador a decrecer, es decir, qué el discriminador comete menos error tendiendo a ganar.

Cálculo de la distribución de probabilidad de los N-grams:

![js_complet](./img/js_complet.png)

La divergencia de Jensen-Shannon (JSD) es una medida de similitud entre dos distribuciones de probabilidad. Se basa en la entropía de la distribución para medir la incertidumbre de un conjunto. La JSD se interpreta como la cantidad de información necesaria para transformar cada una de las dos distribuciones a la media aritmética de las dos, dividida entre 2. Si las dos distribuciones son idénticas, la JSD es cero, mientras que un valor de 1 indica una divergencia máxima y una diferencia máxima entre las dos distribuciones. En este caso se observa como la similitud es alta y que para 20000 iteraciones ya ha dejado de decrecer por lo que el modelo ha aprendido lo suficiente.



### Análisis de las Palabras Generadas

Para analizar el volumne de palabras que puede generar la gan se ha distinguido entre el número de palabras generadas y las que son únicas.

![Unique Words Generated](./img/Unique_Words_Generated.png)

En la gráfica se observa como a medid que se genera un volumen más grande de palabras el porcentaje de contraseñas únicas decrece hasta casi un 40% para el modelo entrenado con 20000 iteraciones. Sin embargo, auque parezca poco que solo el 40% sean contraseñas únicas, hay que considerar que un 40% de 100M es mucho más que un 80% de 1M, por ejemplo.


![Guessing Accuracy Logaritmic](./img/guessing_accuracy_logaritmic.png)

El porcentaje de palabras generadas qué se encuentren en el conjunto de test se tomará como el accuracy. Hay qué apuntar qué no se puede esperar un 80% - 90%, por ello es razonable es conseguir entono a un 5% ya qué esto significa qué se han generado aleatoriamente 5% de las contraseñas qué no se han usado para entrenarlo.

Una de las principales conclusiones que se extraen es que el modelo es capaz de generar palabras que existen en otros idiomas. Esto es especialmente significativo ya que son plabras reales de otros idiomas pero con las que no se le han entrenado. Además, se puede hacer una clasificaión de que idiomas tiene palabras más similares al Español: El portugues es el más parecido seguido de cerca por el Italiano, después el Catalán y luego el Frances.
