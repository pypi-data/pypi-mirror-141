# Author - chris@url.cafe 
# Date - 1645768458

import requests
import haversine

def iss_now(**kwargs)-> dict:
    """This function pulls International Space Station data from http://api.open-notify.org/iss-now.json.
    
       With no paramters this function returns a dict like the following. 
       
        {
         'iss_longitude': -82.64,
         'iss_latitude': 27.76,
         'timestamp': 1646730702,
         'response_message': 'success'
         }
         
         
      
      Parameters[Optional]
      --------------------
      
      
    +--------------+----------+------------------------------------------------------------------------------------------------------+
    |     Name     | Datatype |                                                Notes                                                 |
    +--------------+----------+------------------------------------------------------------------------------------------------------+
    | my_latitude  | Float    | Latitude of the location from which  International Space Station distance needs to be calculated     |
    | my_longitude | Float    | Longitude of the location from which  International Space Station distance needs to be calculated    |
    +--------------+----------+------------------------------------------------------------------------------------------------------+
    
    
    With paramters this function returns a dict like the following.
    
        {
         'iss_longitude': -82.64,
         'iss_latitude': 27.76,
         'timestamp': 1646730702,
         'response_message': 'success',
         'my_longitude': -122.43,
         'my_latitude': 37.77,
         'distance_in_km': 3851.451975831015,
         'distance_in_miles': 2393.181305152873,
         'distance_in_meters': 3851451.975831015
         }
    """
    
    # Making a request to Open-Notify Org and saving the request
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    output=response.json()
    
    # Structuring the response as a dict.
    structured_output={}
    structured_output['iss_longitude']= float(output['iss_position']['longitude'])
    structured_output['iss_latitude']= float(output['iss_position']['latitude'])
    structured_output['timestamp']= output['timestamp']
    structured_output['response_message']= output['message']

    # Checking if optional parameters are plugged in.
    if len(kwargs)>0 :
        
        try:
            
            if((kwargs['my_longitude'] >= -180 and kwargs['my_longitude'] <= 180) and (kwargs['my_latitude'] >= -90 and kwargs['my_latitude'] <= 90 ) ):
                
                # If my_longitude and my_latitude values are within range calculate distance 
                structured_output['my_longitude'] = kwargs['my_longitude']
                structured_output['my_latitude'] = kwargs['my_latitude']
                iss_location=(structured_output['iss_latitude'],structured_output['iss_longitude'])
                my_location=(structured_output['my_latitude'],structured_output['my_longitude'])
                structured_output['distance_in_km']=haversine(iss_location,my_location)
                structured_output['distance_in_miles']=haversine(iss_location,my_location,unit=Unit.MILES)
                structured_output['distance_in_meters']=haversine(iss_location,my_location,unit=Unit.METERS)
                structured_output['note']="Distance is calculated using Haversine formula."
                    

            else:
                structured_output['response_message']= "my_longitude should be between -180 and 180, my_latitude should be between -90 and 90."
        except:
            
            structured_output['response_message']="This module accepts my_latitude and my_longitude as parameters.All other parameters will be rejected."
    
                    
    return structured_output