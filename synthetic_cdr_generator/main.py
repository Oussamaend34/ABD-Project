"""
This is a test file.
"""
from pprint import pprint
from utils import init_pool, load_geography
from generators import VoiceCDRGenerator, SMSCDRGenerator, DataEDRGenerator

if __name__ == "__main__":
    # Load geography data
    cities_data = load_geography()

    # Initialize a pool of random MSISDNs
    POOL_SIZE = 10000
    msisdn_pool = init_pool(POOL_SIZE, cities=cities_data)

    voice_cdr_generator = VoiceCDRGenerator(
        caller_pool=msisdn_pool,
        cities_data=cities_data,
    )
    sms_cdr_generator = SMSCDRGenerator(
        caller_pool=msisdn_pool,
        cities_data=cities_data,
    )
    data_cdr_generator = DataEDRGenerator(
        caller_pool=msisdn_pool,
        cities_data=cities_data,
    )
    pprint(voice_cdr_generator.generate_batch(10))
