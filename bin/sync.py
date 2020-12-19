"""sync
"""
import os
import sys
import pymysql
from datetime import datetime

__author__ = "help@castellanidavide.it"
__version__ = "01.01 2020-12-18"

class sync:
	def __init__ (self, folder=None, debug=False, vs=False):
		"""Where it all begins
		"""
		#Setup basic variabiles
		self.start_time = datetime.now()
		self.debug = debug
		self.vs = vs
		print(folder)

		if folder == None:
			self.folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "flussi")
			print(self.folder)
		else:
			self.folder = folder
		self.log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", f"{self.start_time.strftime('%Y%m%d')}sync.log"), "a+")
		self.local_files = open(os.path.join(self.folder, "file_to_upload_and_where.csv"), "r").read()
		
		self.print(f"Start")
		self.print(f"Opened all files")
		self.print("Running: sync.py")	

		# Sync offline
		self.copy()
		
		# Sync online if possible
		self.online_sync_all()
		try:
			pass
		except:
			self.print("Internet/ DB(s) not avariable")
		
		# End
		self.print(f"End time: {datetime.now()}")
		self.print(f"Total time (python): {datetime.now() - self.start_time}")
		self.log.close()

	def copy(self):
		""" Copy all files in flussi folder
		"""
		try:
			for line in sync.csv2array(self.local_files)[1:]:
				file_path = line[0] + line[1]
				open(os.path.join(self.folder, "cloned", f"""{sync.PC_name()}_{line[1]}"""), "w+").write(open(file_path).read())

			self.print("All files copied offline")
		except:
			self.print("Nothing to copy offline")

	def make_csv_standard(data):
		"""Convert my text in csv standard to prevent errors
		Reference: https://tools.ietf.org/html/rfc4180
		"""
		data.replace(",", "%x2C").replace("}%x2C{", "},{")	# make sure extra commas
		data.replace("\"", "%x22").replace("%x22", "\"", 1).replace("%x22", "\"") # make sure extra double commas
		data.replace("'", '"') # Use " and not ', as csv standard
		data.encode("ASCII")
		return data

	def print(self, item):
		"""Writes on the screen and in the log file
		"""
		if self.debug : print(item)
		self.log.write(f""""{self.start_time.timestamp()}","{item}","{datetime.now().timestamp()}"\n""")

	def PC_name():
		""" Return the PC user-name in standard mode
		"""
		try:
			return os.getlogin().replace(" ", "_")
		except:
			return "PCname"
		
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

	def online_sync_all(self):
		""" If possible update all
		"""
		for i, file in enumerate(sync.csv2array(self.local_files)[1:]):
			self.print(f" - {i}° File")
			
			# Get configuration
			host = file[2]
			port = int(file[3])
			user = file[5]
			password = file[6]
			database = file[4]
			tablename = file[1].replace(".csv", "")

			# Connenct to the DB
			connection = pymysql.connect(host, user, password, database, port)
			self.print(f"   - Connected {i}° database")

			self.sync_online_single(file, connection, database, tablename)

	def sync_online_single(self, file, connection, database, tablename):
		""" Sync a single file
		"""
		with connection.cursor() as cursor:
			file_to_sync = sync.csv2array(open(os.path.join(self.folder, "cloned", f"""{sync.PC_name()}_{file[1]}"""), "r").read())
				
			# If not exist create database
			variabiles = sync.array2csv([[f"""{a.replace(' ', '_')}""" for a in file_to_sync[0]],]).replace('""', '"').replace('"', '').replace('\n', '').replace('\\', '').replace('/', '')

			try:
				cursor.execute(f"""CREATE TABLE {database}.{tablename} (ID int AUTO_INCREMENT,{str([i+' varchar(255),' for i in variabiles.split(",")])[1:-1].replace("', '", "")},PRIMARY KEY (ID));""")
			except:
				cursor.execute(f"""CREATE TABLE {tablename} (ID int AUTO_INCREMENT,{str([i+' varchar(255),' for i in variabiles.split(",")])[1:-1].replace("', '", "")},PRIMARY KEY (ID));""")
			self.print(f"   - Connected {tablename} table")

			# Add all new items
			for j, items in enumerate(file_to_sync[1:]):
				items = sync.array2csv([items,])[:-1:]

				try:
					cursor.execute(f"SELECT * FROM {database}.{tablename} WHERE ({variabiles}) = ({items});")
				except:
					cursor.execute(f"SELECT * FROM {tablename} WHERE ({variabiles}) = ({items});")
				if len(cursor.fetchall()) == 0: # If not exist add it
					try:
						cursor.execute(f"INSERT INTO {database}.{tablename} ({variabiles}) VALUES ({items});")
					except:
						cursor.execute(f"INSERT INTO {tablename} ({variabiles}) VALUES ({items});")
					self.print(f"   - Values added ({items})")

		# Push changes
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

	sync(debug=debug, vs=vs)
