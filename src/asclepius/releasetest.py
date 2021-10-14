# import Asclepius dependencies
from asclepius.instelling import GGZ, ZKH
from asclepius.medewerker import Medewerker
from asclepius.portaaldriver import PortaalDriver
from asclepius.testen import TestFuncties, Verklaren

# import other dependencies
from typing import Union
from pandas import ExcelWriter

class ReleaseTesten:

    def __init__(self, gebruiker: Medewerker, *producten: str, losse_bestanden: bool = False):
        
        # Te testen
        self.da = False
        self.bi = False
        self.zpm = False

        # Initialiseren
        self.gebruiker = gebruiker
        self.portaaldriver = PortaalDriver(self.gebruiker, producten)
        self.testfuncties = TestFuncties()
        self.verklaren = Verklaren()

        self.losse_bestanden = losse_bestanden

        self.update_producten(producten)
        return None

    def update_producten(self, *producten):
        if 'da' in producten:
            self.da = True
        else: pass
        if 'bi' in producten:
            self.bi = True
        else: pass
        if 'zpm' in producten:
            self.zpm = True
        else: pass
        return None

    def test(self, *instellingen: Union[GGZ, ZKH]):
        mislukt_download = []
        mislukt_da = []
        mislukt_bi = []
        mislukt_zpm = []

        # -------------- DOWNLOAD EXCELS --------------

        # Download de relevante excels voor alle instellingen
        for instelling in instellingen:
            try:
                self.portaaldriver.webscraper(instelling)
            except:
                mislukt_download.append(instelling.klant_code)
        

        # -------------- TEST DA, BI, ZPM --------------
        
        # Test de instellingen waarvan de files correct zijn gedownload
        for instelling in instellingen:
            if instelling.klant_code not in set(mislukt_download):

                # Test DA
                if self.da and instelling.da:
                    try:
                        self.test_da(instelling)
                    except:
                        mislukt_da.append(instelling.klant_code)
                else:
                    pass

                # Test BI
                if self.bi and instelling.bi:
                    try:
                        self.test_bi(instelling)
                    except:
                        mislukt_bi.append(instelling.klant_code)
                else:
                    pass

                # Test ZPM
                if self.zpm and instelling.zpm:
                    try:
                        self.test_zpm(instelling)
                    except:
                        mislukt_zpm.append(instelling.klant_code)
                else:
                    pass


        # -------------- PRINT RESULTATEN --------------
        # print de resultaten van de DA test
        if self.da and self.losse_bestanden:
            for instelling in instellingen:
                if instelling.klant_code not in set(mislukt_download + mislukt_da) and instelling.da:
                    with ExcelWriter(f'Bevindingen DA {instelling.klant_code}.xlsx') as writer:
                        instelling.bevindingen_da.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                        instelling.bevindingen_da_test.to_excel(writer, sheet_name=f'{instelling.klant_code} test')
                else: pass
        elif self.da:
            with ExcelWriter(f'Bevindingen DA.xlsx') as writer:
                for instelling in instellingen:
                    if instelling.klant_code not in set(mislukt_download + mislukt_da) and instelling.da:
                        instelling.bevindingen_da.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                        instelling.bevindingen_da_test.to_excel(writer, sheet_name=f'{instelling.klant_code} test')
                    else: pass
        else: pass
        
        if self.bi and self.losse_bestanden:
            for instelling in instellingen:
                if instelling.klant_code not in set(mislukt_download + mislukt_bi) and instelling.bi:
                    with ExcelWriter(f'Bevindingen BI {instelling.klant_code}.xlsx') as writer:
                        instelling.bevindingen_bi.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                else: pass
        elif self.bi:
            with ExcelWriter(f'Bevindingen BI.xlsx') as writer:
                for instelling in instellingen:
                    if instelling.klant_code not in set(mislukt_download + mislukt_bi) and instelling.bi:
                        instelling.bevindingen_bi.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                    else: pass
        else: pass
        
        if self.zpm and self.losse_bestanden:
            for instelling in instellingen:
                if instelling.klant_code not in set(mislukt_download + mislukt_zpm) and instelling.zpm:
                    with ExcelWriter(f'Bevindingen ZPM {instelling.klant_code}.xlsx') as writer:
                        instelling.bevindingen_zpm.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                else: pass
        elif self.zpm:
            with ExcelWriter(f'Bevindingen ZPM.xlsx') as writer:
                for instelling in instellingen:
                    if instelling.klant_code not in set(mislukt_download + mislukt_zpm) and instelling.zpm:
                        instelling.bevindingen_zpm.to_excel(writer, sheet_name=f'{instelling.klant_code}')
                    else: pass
        else: pass


        # -------------- MISLUKTE INSTELLINGEN --------------

        if len(mislukt_download) != 0:
            print('Mislukte downloads:', ' '.join(mislukt_download))
        else:
            print('Geen mislukte downloads!')
        
        if self.da and len(mislukt_da) != 0:
            print('Mislukte DA tests:', ' '.join(mislukt_da))
        elif self.da:
            print('Geen mislukte DA tests!')
        else: pass

        if self.bi and len(mislukt_bi) != 0:
            print('Mislukte BI tests:', ' '.join(mislukt_bi))
        elif self.bi:
            print('Geen mislukte BI tests!')
        else: pass

        if self.zpm and len(mislukt_zpm) != 0:
            print('Mislukte ZPM tests:', ' '.join(mislukt_zpm))
        elif self.zpm:
            print('Geen mislukte ZPM tests!')
        else: pass

        # einde van test()
        return None
    
    def test_da(self, instelling: Union[GGZ, ZKH]):
        # Aantallencheck
        self.testfuncties.aantallencheck(instelling, False)
        self.testfuncties.aantallencheck(instelling, True)

        # Standaardverschillen vinden
        self.verklaren.standaardverschillen_da(instelling, False)
        self.verklaren.standaardverschillen_da(instelling, True)
        return None
    
    def test_bi(self, instelling: Union[GGZ, ZKH]):
        self.testfuncties.prestatiekaarten_vergelijken(instelling, 'bi')
        return None
    
    def test_zpm(self, instelling: Union[GGZ, ZKH]):
        self.testfuncties.prestatiekaarten_vergelijken(instelling, 'zpm')
        return None
    
