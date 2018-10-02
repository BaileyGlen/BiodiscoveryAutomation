import unittest
from auto_microarray import validateAscessionNumber, validatePatientName, validateMRN, matchFiles
class TestPatientName(unittest.TestCase):
    def test_validatePatientName(self):
        namelist = ["wright wallace, zach"]
        for name in namelist:
            self.assertTrue (validatePatientName(name))
    def test_blank(self):
        self.assertFalse (validatePatientName(" "))
    def test_number(self):
        self.assertFalse (validatePatientName("Wr1ght Wallace, Zach"))
        self.assertFalse (validatePatientName("Wright Wallace, Z4ch"))
    def test_commas(self):
        self.assertFalse (validatePatientName("Wright Wallace Zach"))
        self.assertFalse (validatePatientName("Wright, Wallace, Zach"))          
class TestAscessionNumber(unittest.TestCase):
    def test_validateAscessionNumber(self):
        numlist=["AB18-5320"]
        for num in numlist:
            print(num)
            assert (validateAscessionNumber(num))
    def test_badfirst(self):
        self.assertFalse (validateAscessionNumber("1234-1234"))
    def test_badsecond(self):
        self.assertFalse (validateAscessionNumber("AB34-CD34"))
    def test_dashes(self):
        self.assertFalse (validateAscessionNumber("AB-34-1234"))
        self.assertFalse (validateAscessionNumber("AB341234"))
    def test_toolittle(self):
        self.assertFalse (validateAscessionNumber("A12-1234"))
    def test_toomany(self):
        self.assertFalse (validateAscessionNumber("A123-1234"))
class TestMRN(unittest.TestCase):
    def test_alpha(self):
        self.assertFalse (validateMRN("00A8907"))
class TestMatchFiles(unittest.TestCase):
    def test_matching(self):
        #testing if file is there
        self.assertTrue (matchFiles("CG18-716",["Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_2_CG18-692.txt","Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_6_CG18-716.txt"]))
        #testing if file isn't there
        self.assertFalse (matchFiles("CG18-716",["Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_2_CG18-692.txt","Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_8_CG18-723.txt"]))
        #testing if it finds mulitple
        self.assertTrue (matchFiles("CG18-716",["Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_6_CG18-716.txt","Z:\\MicroArray\Archived data\GS projects\GS PROJECTS 2018\6-5-2018 32PAT\6-5-2018 32PAT_Custom_nexus_input_6_CG18-716.txt"]))
if(__name__=='__main__'):
    unittest.main()