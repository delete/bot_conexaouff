import logging

def log(message):
	filename = '.meulog.log'
	logging.basicConfig(filename=filename,
						format='%(asctime)s %(levelname)-6s %(message)s')

	logging.debug(message)