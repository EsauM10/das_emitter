from typing import Literal

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from das_emitter.selenium import DownloadManager, SeleniumDriver
from das_emitter.exceptions import (
    AuthenticationException, InvalidCNPJException, 
    MonthNotAvailableException, YearNotAvailableException
)

MonthType = Literal[
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro'
]

class DASEmitter:
    def __init__(self) -> None:
        self.url = 'https://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app'
        self.driver = SeleniumDriver(headless=False)
        self.download_manager = DownloadManager(self.driver.download_path)
        
    def __get_toast_message(self) -> str:
        try:
            return self.driver.await_element('//div[@class="toast-message"]').text
        except TimeoutException:
            return 'Tempo expirado'
    
    def __fill_cnpj_input(self, cnpj: str):
        cnpj_input = self.driver.await_element('//input[@id="cnpj"]', timeout=10)
        cnpj_input.send_keys(cnpj) 

    def __click_continue_button(self):
        button_submit = self.driver.await_element('//button[@id="continuar"]')
        button_submit.click()

    def __await_homepage_load(self):
        try:
            self.driver.await_element('//strong[text()="PRIMEIRO PAGAMENTO EM DIA"]', timeout=10)
        except TimeoutException:
            message = self.__get_toast_message()
            if(message == 'CNPJ inválido.'):
                raise InvalidCNPJException(message)
            raise AuthenticationException(message)

    def __click_select_year_button(self):
        self.driver.await_element('//button[@data-id="anoCalendarioSelect"]', timeout=5).click()
    
    def __select_year(self, year: int):
        listbox = self.driver.await_element('//ul[@role="listbox"]')
        enabled_items = listbox.find_elements(By.XPATH, 'li[not(contains(@class, "disabled"))]')

        for item in enabled_items:
            if(item.text == str(year)):  
                item.click()
                self.driver.await_element('//button[@type="submit"]').click()
                break
        else:
            raise YearNotAvailableException(f'Ano de "{year}" indisponível')

    def __select_month(self, month: MonthType):
        table = self.driver.await_element('//div[@id="resumoDAS"]/table', timeout=5)
        month_tbody_list = table.find_elements(By.XPATH, 'tbody')[1:]

        for tbody in month_tbody_list:
            if(month.capitalize() in tbody.text):
                tbody.find_element(By.XPATH, 'tr/td[@class="selecionar text-center"]').click()
                break
        else:
            raise MonthNotAvailableException(f'Mês de "{month}" indisponível')

    def __click_generate_button(self):
        self.driver.await_element('//button[@id="btnEmitirDas"]').click()

    def __click_print_button(self):
        link_xpath = f'//a[@href="/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/emissao/imprimir"]'
        self.driver.await_element(link_xpath, timeout=10).click()

    def __get_downloaded_file(self, cnpj: str, year: int) -> bytes:
        filename = f'DAS-PGMEI-{cnpj}-AC{year}.pdf'
        data = self.download_manager.await_download_file(filename)
        self.download_manager.delete_file(filename)
        return data

    def get_pdf(self, cnpj: str, month: MonthType, year: int) -> bytes:
        try:
            self.driver.goto(f'{self.url}/Identificacao')
            self.__fill_cnpj_input(cnpj)
            self.__click_continue_button()
            self.__await_homepage_load()
            self.driver.goto(f'{self.url}/emissao')
            self.__click_select_year_button()
            self.__select_year(year)
            self.__select_month(month)
            self.__click_generate_button()
            self.__click_print_button()
            return self.__get_downloaded_file(cnpj, year)
        
        except Exception as ex:
            raise ex
        finally:
            self.driver.close()
