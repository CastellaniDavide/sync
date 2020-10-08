"""sync
"""
import os
import sys
import pymysql
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2020-10-04"

class sync:
	def __init__ (self, debug=False, db=True, vs=False):
		"""Where it all begins
		"""
		base_dir = "." if vs else ".." # the project "root" in Visual studio it is different

		log = open(os.path.join(base_dir, "log", "trace.log"), "a+")
		local_files = open(os.path.join(base_dir, "flussi", "file_to_upload_and_where.csv"), "r").read()
		sync.log(log, "Opened all files")
		
		start_time = datetime.now()
		sync.log(log, f"Start time (python): {start_time}")
		sync.log(log, "Running: sync.py")

		# Sync offline
		sync.copy(local_files, base_dir, log, debug)
		
		# Sync online if possible
		try:
			sync.sync(local_files, base_dir, log, debug)
		except:
			sync.print_and_log(log, "Internet/ DB(s) not avariable", debug)
		
		# End
		sync.log(log, f"End time: {datetime.now()}\nTotal time (python): {datetime.now() - start_time}")
		if debug : sync.log(log, "")
		log.close()

	def copy(local_files, base_dir, log, debug):
		""" Copy all files in flussi folder
		"""
		
		for line in sync.csv2array(local_files)[1:]:
			file_path = line[0] + line[1]
			open(os.path.join(base_dir, "flussi", "cloned", f"""{sync.PC_name()}_{line[1]}"""), "w+").write(open(file_path).read())

		sync.print_and_log(log, "All files cloned", debug)

	def make_csv_standard(data):
		"""Convert my text in csv standard to prevent errors
		Reference: https://tools.ietf.org/html/rfc4180
		"""
		data.replace(",", "%x2C").replace("}%x2C{", "},{")	# make sure extra commas
		data.replace("\"", "%x22").replace("%x22", "\"", 1).replace("%x22", "\"") # make sure extra double commas
		data.replace("'", '"') # Use " and not ', as csv standard
		data.encode("ASCII")
		return data

	def log(file, item):
		"""Writes a line in the log.log file
		"""
		file.write(f"{item}\n")

	def print_and_log(file, item, debug):
		"""Writes on the screen and in the log file
		"""
		if debug : print(item)
		sync.log(file, item)

	def init_csv(flie, intestation, log):
		"""Init the csv files
		"""
		flie.write(f"{intestation}\n")
		sync.log(log, "csv now initialized")

	def print_db(db_file, intestation, log, debug, tablename_main="sync"):
		"""Checks the database content
		"""
		# Main content
		if debug : print("\nDatabase main content:")
		if debug : print(intestation.replace("\\\\", "\\"))

		for row in db_file.execute(f"SELECT * FROM {tablename_main}").fetchall():
			if debug : print(str(row)[1:-1].replace("'", "").replace("\\\\", "\\").replace("\\\\", "\\"))

	def PC_name():
		""" Return the PC user-name in standard mode
		"""
		return os.getlogin().replace(" ", "_")
		
	def csv2array(csv):
		""" Converts csv file to a py array
		"""
		array = []
		item_valid = True

		for line in csv.split("\n"):
			temp = []
			item = ""
			for char in (line + ","):
				if char == "," and item_valid:
					temp.append(item.replace("\\\\", "\\"))
					item = ""
				elif char == '"':
					if item_valid:
						item_valid = False
					else:
						item_valid = True
				else:
					item += char

			if len(temp) > 1:
				array.append(temp)

		return array

	def array2csv(array):
		""" Converts py array to a csv file
		"""
		text = ""

		for line in array:
			for item in line:
				text += f'"{item}",'
			text = text[:-1:] + "\n"

		return text

	def sync(local_files, base_dir, log, debug):
		""" If possible update all
		"""
		for i, file in enumerate(sync.csv2array(local_files)[1:]):
			sync.print_and_log(log, f" - {i}° File", debug)
			
			host = file[2]
			user = file[4]
			password = file[5]
			database = file[3]
			tablename = file[1].replace(".csv", "")
			connection = pymysql.connect(host, user, password, database)
			sync.print_and_log(log, f"   - Connected {i}° database", debug)

			with connection.cursor() as cursor:
				file_to_sync = sync.csv2array(open(os.path.join(base_dir, "flussi", "cloned", f"""{sync.PC_name()}_{file[1]}"""), "r").read())
				
				# If not exist create database
				variabiles = sync.array2csv([[f"""{a.replace(' ', '_')}""" for a in file_to_sync[0]],]).replace('""', '"').replace('"', '').replace('\n', '').replace('\\', '').replace('/', '')
				variabiles_with_type = sync.array2csv([[f"""{a.replace(' ', '_')} varchar(255)""" for a in file_to_sync[0]],]).replace('""', '"').replace('"', '').replace('\n', '').replace('\\', '').replace('/', '')

				cursor.execute(f"""CREATE TABLE IF NOT EXISTS {tablename} (ID int AUTO_INCREMENT, {variabiles_with_type}, PRIMARY KEY (ID));""")
				sync.print_and_log(log, f"   - Connected {i}° table", debug)

				# Add all new items
				for j, items in enumerate(file_to_sync[1:]):
					items = sync.array2csv([items,])[:-1:]

					cursor.execute(f"SELECT * FROM {tablename} WHERE ({variabiles}) = ({items});")
					if len(cursor.fetchall()) == 0:
						cursor.execute(f"INSERT INTO {tablename} ({variabiles}) VALUES ({items});")
						sync.print_and_log(log, f"   - Values added ({items})", debug)

			connection.commit()
			connection.close()

if __name__ == "__main__":
	# debug flag
	debug = True

	# visual studio flag
	vs = True

	# database flag
	db = True

	# check if is launched by .bat file
	if "--batch" in sys.argv or "-b" in sys.argv:
		debug = False
		vs = False

	sync(debug, db, vs)
