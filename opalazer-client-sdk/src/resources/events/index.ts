// src/resources/events/index.ts

import { AxiosResponse } from 'axios';
import { Base } from '../base';
import { EventSchemaIn, WindowLocation, Browser  } from './types';

const resourceName = 'v1/events';

interface UserLocation{
    latitude:number
    logitude:number
    accuracy: number
}

const geo_options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  };

async function get_geo_location(): Promise<GeolocationCoordinates | any> {
    if (navigator.geolocation){
        navigator.geolocation.getCurrentPosition((pos) => {
          return pos.coords
        },(error) => {
          switch(error.code) {
            case error.PERMISSION_DENIED:
              console.log("User denied the request for Geolocation.")
              break;
            case error.POSITION_UNAVAILABLE:
              console.log("Location information is unavailable.")
              break;
            case error.TIMEOUT:
              console.log("The request to get user location timed out.")
              break;
          }
        },geo_options);
      } else {
        console.log("Your browser doesn't support geolocation.")
      }
    return null
}

export class OpalEvents extends Base {

  async create_opal_event(newEvent: EventSchemaIn | undefined): Promise<AxiosResponse<EventSchemaIn, any>> {
    let e = {} as EventSchemaIn
    let g = {} as GeolocationCoordinates
    g = await get_geo_location()
    e.latitude = g.latitude
    e.longitude = g.longitude
    e.accuracy = g.accuracy
    e.window_location_json = window.location
    return this.API.post<EventSchemaIn>(`/${resourceName}`, {
      method: 'POST',
      body: JSON.stringify(newEvent),
    });
  }
}
