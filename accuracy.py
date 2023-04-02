import os
import argparse
import numpy as np
import pickle
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-generated', '-g',
                        dest='input_generated',
                        help='The generated text file')

    parser.add_argument('--input-test', '-t',
                        dest='input_test',
                        help='The test file for comparison')
    
    parser.add_argument('--input-duplicates', '-d',
                        dest='input_duplicates',
                        help='The file containing passwords in both test and generated file')
    
    parser.add_argument('--n-passwords', '-p',
                        dest='n_passwords',
                        help='The number of passwords read from the file.')

    parser.add_argument('--n-passwords-vec', '-pv',
                        nargs='+',
                        dest='n_passwords_vec',
                        help='Array containing the number of passwords read from the file.')

    return parser.parse_args()

args = parse_args()

"""
def accuracy(path_generated, path_test, n_passwords=10**8):
    #generated_file = open(path_generated, 'r').readlines()
    with open(path_generated, 'r') as myfile:
        generated_file = [next(myfile) for x in range(int(n_passwords))]
    #test_data = open(path_test, 'r').readlines()
    with open(path_test, 'r') as myfile:
        test_data = [next(myfile) for x in range(int(n_passwords))]  
    generated_data = set(generated_file)
    test_data = set(test_data)
    #print("The number of unique password generated is {}.". format(len(generated_data)))
    #print("The number of unique password in the test set is {}.". format(len(test_data)))
    overlap = generated_data & test_data
    #print("{} passwords are correctly guessed.".format(len(overlap)) )
    result = round(float(len(overlap))/len(test_data) * 100, 4)
    result_df=pd.DataFrame({"path_generated":[path_generated], \
        "path_test":[path_test], \
        "n_passwords":[n_passwords], \
        "n_unique_generated_passwords":[len(generated_data)], \
        "n_unique_test_passwords":[len(test_data)], \
        "overlap":[len(overlap)], \
        "guessing accuracy":[result]})
    #print('The guessing accuracy is {} %'.format(result))
    return result_df
 """   

def accuracy_vec(path_generated, path_test, n_passwords_vec):
    df=pd.DataFrame({})

    #leer contraseñas
    generated_file = open(path_generated, 'r').readlines()
    test_data = open(path_test, 'r').readlines()
    test_data = set(test_data)
         
    for n_passwords in n_passwords_vec:

        generated_data = set(generated_file[:int(n_passwords)])
        overlap = generated_data & test_data
        result = round(float(len(overlap))/len(test_data) * 100, 4)
        result_df=pd.DataFrame({"path_generated":[path_generated], \
            "path_test":[path_test], \
            "n_passwords":[n_passwords], \
            "n_unique_generated_passwords":[len(generated_data)], \
            "n_unique_test_passwords":[len(test_data)], \
            "overlap":[len(overlap)], \
            "guessing accuracy":[result]})
        df=pd.concat([df,result_df])

    #Guardar resultados
    report_name='/'.join(path_generated.split('/')[0:-1])+"/report.csv"
    try:
        df_extend=pd.concat([pd.read_csv(report_name),df])
        df_extend.to_csv(report_name, index=False)
    except FileNotFoundError:
        df.to_csv(report_name, index=False)
        

    return 
accuracy_vec(args.input_generated, args.input_test,args.n_passwords_vec)


    
