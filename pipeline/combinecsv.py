import os
import glob
import pandas as pd

def combcsv(dir, finalname):
	os.chdir(dir)
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

	#combine all files in the list
	combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

	#export to csv
	combined_csv.to_csv( finalname, index=False, encoding='utf-8-sig')