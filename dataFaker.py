#!/usr/bin/env python3

#===========================================================#
#File Name:			dataFaker.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@gmail.com
#Creation Date:		Thu Sep 25 09:16:16 2025
#Last Modified:		Thu Sep 25 09:16:17 2025
#Description:
#Args:
#Usage:
#===========================================================#

from faker import Faker
import random
import pandas as pd
import uuid
import argparse

def generate_car_data(fake):
	"""Generate fake car data with specified fields"""
	
	# Brazilian car brands
	marcas = ['VOLKSWAGEN', 'CHEVROLET', 'FIAT', 'FORD', 'HYUNDAI', 'TOYOTA', 'HONDA', 'NISSAN', 'RENAULT', 'PEUGEOT']
	
	# Models by brand (simplified)
	modelos = {
		'VOLKSWAGEN': ['GOL', 'POLO', 'T-CROSS', 'JETTA', 'TIGUAN'],
		'CHEVROLET': ['ONIX', 'PRISMA', 'CRUZE', 'TRACKER', 'S10'],
		'FIAT': ['UNO', 'ARGO', 'MOBI', 'TORO', 'STRADA'],
		'FORD': ['KA', 'ECOSPORT', 'FOCUS', 'RANGER', 'TERRITORY'],
		'HYUNDAI': ['HB20', 'CRETA', 'TUCSON', 'ELANTRA', 'SANTA FE'],
		'TOYOTA': ['ETIOS', 'YARIS', 'COROLLA', 'RAV4', 'HILUX'],
		'HONDA': ['FIT', 'CITY', 'CIVIC', 'HR-V', 'CR-V'],
		'NISSAN': ['MARCH', 'VERSA', 'SENTRA', 'KICKS', 'FRONTIER'],
		'RENAULT': ['KWID', 'LOGAN', 'SANDERO', 'DUSTER', 'CAPTUR'],
		'PEUGEOT': ['208', '2008', '308', '3008', '5008']
	}
	
	marca = fake.random_element(marcas)
	modelo = fake.random_element(modelos[marca])
	ano = fake.random_int(min=2000, max=2025)
	motorizacao = fake.random_element(['1.0', '1.4', '1.6', '2.0', '2.4', '3.0'])
	combustivel = fake.random_element(['FLEX', 'GASOLINA', 'DIESEL', 'HÍBRIDO', 'ELÉTRICO'])
	cor = fake.color_name()
	quilometragem = fake.random_int(min=0, max=200000)
	portas = fake.random_element([2, 4, 5])
	transmissao = fake.random_element(['MANUAL', 'AUTOMÁTICA', 'CVT'])
	estado = fake.random_element(['NOVO', 'SEMINOVO', 'USADO EXCELENTE', 'USADO MUITO BOM', 'USADO BOM', 'USADO REGULAR', 'USADO RUIM'])
	timestamp = fake.date_time_between(start_date='-25y')
	
	return {
		'brand': marca,
		'model': modelo,
		'year': ano,
		'engine': motorizacao,
		'fuel': combustivel,
		'color': cor,
		'mileage': quilometragem,
		'number_doors': portas,
		'transmission': transmissao,
		'condition': estado,
		'date_added': timestamp
	}


def main(argv):
	parser = argparse.ArgumentParser(description="Generate fake car data.")
	parser.add_argument("number_cars", type=int, help="Number of car samples to generate")
	parser.add_argument("--lang", type=str, default="pt_BR", help="Language locale for Faker (default: pt_BR)")
	parser.add_argument("--output", type=str, default="cars.csv", help="Output CSV file name (default: cars.csv)")
	args = parser.parse_args(argv)

	fake = Faker(args.lang)
	number_cars = args.number_cars
	output_file = args.output

	rows = []
	for _ in range(number_cars):
		car_data = generate_car_data(fake)
		row = {'id': uuid.uuid4()}
		for field, value in car_data.items():
			row[field] = value
		rows.append(row)
	
	df = pd.DataFrame(rows)
	df.to_csv(output_file, index=False)

	print("Dados de Carros Gerados:", len(df))


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


