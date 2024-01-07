#IMPORTANDO MÓDULOS SELENIUM
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

import time

#IMPORTANDO MÓDULOS ENVIO DE E-MAILS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#CONFIGURAÇÃO DO CHROME (NÃO FECHAR A TELA E INICIAR MAXIMIZADO)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")

#INSTALANDO O CHROMEDRIVER SE PRECISAR E PASSANDO OS PARÂMETROS DE OPÇÕES E ATUALIZAÇÕES
#PARA O WEBDRIVER
servico = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=servico, options=chrome_options)

browser.implicitly_wait(3) #Aguarda até 3 segundos cada etapa para os elementos aparecerem

class param: #PARÂMETROS DE ACESSO
    #LINKEDIN
    usuario = "nicolas-lemos@outlook.com"
    senha = "nicolas2005"

    #E-MAIL
    remetente = 'nicolas-lemos@outlook.com'
    senhaEmail = 'nicolas2005'
    destinatario = 'nicolaslemosaparecido@gmail.com'

class login: #Realizando login no LinkedIn
    @staticmethod
    def linkedin(usuario,senha):                                                  #Função Login LinkedIn
        browser.get("https://br.linkedin.com/")                                         #Acessando a Página
        browser.find_element(By.ID,"session_key").send_keys(usuario)                    #Inserindo Usuário
        browser.find_element(By.XPATH,"//*[@id='session_password']").send_keys(senha)   #Inserindo Senha
        browser.find_element(By.XPATH,"//*[@data-id='sign-in-form__submit-btn']").click()

class acesso: #Acessando site e post
    @staticmethod
    def site():
        browser.find_element(By.XPATH,"//*[@class='t-16 t-black t-bold']").click()      #Entrando Perfil
        browser.find_element(By.XPATH,"//span[text()='Exibir projeto']").click()        #Entrando no site

    def post():
        browser.get("https://sites.google.com/view/nicolaslemos/home")                  #Acessando Página
        browser.find_element(By.XPATH,"//span[text()='Sensor Ultrassônico (Proximidade)']").click()
        img = browser.find_element(By.XPATH,"//*[@id='h.4e4cb108ea4a2693_216']")        #Encontrando Imagem
        img.screenshot("image.png")                                                     #Armazenando Print

class email: #Enviando e-mail usando smtplib e MIME
    @staticmethod
    def enviando(remetente,destinatario,senhaEmail):
        fromaddr = remetente
        toaddr = destinatario
        msg = MIMEMultipart()

        msg['From'] = fromaddr 
        msg['To'] = toaddr
        msg['Subject'] = "Envio de Arquivos Solicitados 03/01/2024"                     #Assunto do E-mail

        #Corpo da Mensagem
        body = "\nPrezado,\n\nVenho, a partir deste email, enviar em anexo o arquivo solicitado.\n\nAtenciosamente"         
        
        msg.attach(MIMEText(body, 'plain'))

        #Anexo a ser enviado
        filename = 'image.png'
        attachment = open('image.png','rb')

        #Convertendo Arquivo para Base64
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        attachment.close()

        #Servidor SMTP do Outlook e Passagem dos Argumentos
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()
        server.login(fromaddr, senhaEmail)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        print('\nEmail enviado com sucesso!')


login.linkedin(param.usuario,param.senha) 
time.sleep(15) #Tempo de Espera para realizar o recaptcha
acesso.site()
acesso.post()
email.enviando(param.remetente,param.destinatario,param.senhaEmail)
