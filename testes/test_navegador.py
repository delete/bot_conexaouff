# coding: utf-8
import unittest
import mechanize
import json
import os

from classes.Navegador import Navegador


class NavegadorSuccessTest(unittest.TestCase):

	def setUp(self):
		self.browser = Navegador()
		self.browser.setUrl('https://sistemas.uff.br/conexaouff')

	def tearDown(self):
		self.browser.exit()

	def test_object(self):
		self.assertIsInstance(self.browser, Navegador)

	def test_url(self):
		self.assertEqual(self.browser.url, 'https://sistemas.uff.br/conexaouff')

	def test_page_content(self):
		self.assertIn('Bem vindo ao Portal IDUFF', self.browser.getContent())		
	
	#@unittest.skip('This test is slow...')
	def test_login(self):		
		self.browser.login()
		self.assertIn('Meus Grupos', self.browser.getContent())
		self.assertIn('Tópicos respondidos', self.browser.getContent())



class NavegadorEmptyTest(unittest.TestCase):

	def setUp(self):
		self.browser = Navegador()		

	def tearDown(self):
		self.browser.exit()

	def test_if_url_is_none(self):
		self.assertEqual(self.browser.url, None)

	def test_page_content(self):
		self.assertEqual(self.browser.getContent(), None)

	def test_login_without_url(self):
		self.assertRaises(mechanize.BrowserStateError, self.browser.login)


class NavegadorErrorTest(unittest.TestCase):
	
	def setUp(self)	:
		self.browser = Navegador()
		self.browser.setUrl('https://sistemas.uff.br/conexaouff')

		data = {
			'username': '123456',
			'password': '654321',
			}
		with open('testFile', 'w') as outfile:
  			json.dump(data, outfile)

  		self.browser.setLoginFile('testFile')

  	def tearDown(self):
  		os.remove('testFile')
  		self.browser.exit()

  	#@unittest.skip('This test is slow...')
	def test_invalid_login(self):
		self.browser.login()
		self.assertIn('CPF ou senha inválido. Por favor, tente novamente.', self.browser.getContent())

	def test_without_login_file(self):
		self.browser.setLoginFile('')		
		self.assertRaises(IOError, self.browser.login)


if __name__ == '__main__':
	unittest.main()