from django.test import TestCase
from fttrackerapp.data_fetchers import FoodTruckDataFetcher
from django.test import TestCase

from fttrackerapp.models import FoodTruck, Location, Appearance
from datetime import date
import json

class FoodTruckDataFetcherTests(TestCase):
    def setUp(self):
        pass

    def test_single_event_parser(self):
        """
        Test the Data fetcher's ability to
        parse the json representation of an
        event
        """
        sample_json_str = """{"id":"1422570727976584","owner":{"category":"Food\/beverages","category_list":[{"id":"2252","name":"Food\/Beverages"}],"name":"Off the Grid","id":"129511477069092"},"name":"Off the Grid: Lake Merritt  (Friday Dinner)","description":"Join OMCA and Off the Grid on 10th Street every Friday for a family-friendly take on a festive night market. This Friday Night, celebrate all things in art and education with Creative Impact, an on-site event with public live performances featuring youth arts organizations, and a resource fair open to all! Savor California beer and wine around the Koi Pond while enjoying live music, art activities, dancing, and more! Bring the whole family to OMCA for a sampling of the best in Bay Area curbside cuisine\u2014and all that OMCA has to offer!\\n\\nLocation: 1000 Oak Street, Oakland, CA 94607 \\nDirections: OMCA is located one block from the Lake Merritt BART Station. Exit the station and walk east towards Laney College and\/or Lake Merritt. Event parking at the OMCA Garage for a $5 flat fee, after 5 pm. http:\/\/museumca.org\/how-\u00ad\u2010get-\u00ad\u2010here\\nTime: 5:00pm - 9:00pm\\n--\\nGallery admission after 5pm: Half-\u00ad\u2010off admission for Adults, ages 18 and under are free. Admission for Members is always free. Admissions desk is located on Level 2. Please note that as of September 4, 2014 OMCA gallery admission ticket prices increased: General Adult: $15; Senior & Student: $10; Youth age 9 \u2013 17: $6; and Children 8 & under: Free. http:\/\/museumca.org\/hours-\u00ad\u2010admission\\n\\nAdditional Amenities included:\\n\u2022 Restrooms: Public access to restrooms located on Levels 1, 2 & 3\\n\u2022 ATM machine: Level 2 across from restrooms\\n\u2022 Our Building: http:\/\/museumca.org\/our-\u00ad\u2010building\\n\u2022 Facility Rental Program: http:\/\/museumca.org\/rent-\u00ad\u2010museum\\n\\nCost: Half-price gallery admission for adults, ages 18 and under are free. Admission for Members is always free. Cash bar. Prices vary for Off the Grid food trucks.\\n\\nVendors:\\nArKi Truck\\nCupkates\\nGo Streatery\\nGrilled Cheese Bandits\\nHapa SF\\nKasa Indian\\nLiba Falafel\\nLittle Green Cyclo\\nSanguchon\\nSenor Sisig\\nThe Chairman\\nWhip Out\\n\\nCATERING NEEDS? Have OtG cater your next event! Get started by visiting offthegridsf.com\/catering.","start_time":"2013-12-20T17:00:00-0800","end_time":"2013-12-20T21:00:00-0800","timezone":"America\/Los_Angeles","is_date_only":false,"location":"1000 Oak St, Oakland CA","venue":{"name":"1000 Oak St, Oakland CA"},"privacy":"OPEN","updated_time":"2013-12-13T00:41:41+0000"}"""
        sample_json = json.loads(sample_json_str)
        location, vendor_list, appearance_date = FoodTruckDataFetcher()._FoodTruckDataFetcher__parse_event_json(sample_json)
        # Test location
        self.assertEqual(location,"1000 Oak St, Oakland CA","Failed to parse location.")

        # Test vendor list
        expected_list = ['ArKi Truck', 'Cupkates', 'Go Streatery', 'Grilled Cheese Bandits', 'Hapa SF', 'Kasa Indian', 'Liba Falafel', 'Little Green Cyclo', 'Sanguchon', 'Senor Sisig', 'The Chairman', 'Whip Out']
        test_passed = True
        for vendor in expected_list:
            if vendor not in vendor_list:
                test_passed = False
        self.assertTrue(test_passed, "Failed to parse vendor list")

        # Test date
        self.assertEqual(appearance_date,date(2013,12,20), "Failed to parse date")
