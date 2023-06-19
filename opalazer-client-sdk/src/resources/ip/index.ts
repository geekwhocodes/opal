// src/resources/ip/index.ts

import { AxiosResponse } from 'axios';
import { Base } from '../base';
import { Ip } from './types';

export class OpalIp extends Base {
  get_ip(): Promise<AxiosResponse<Ip, any>> {
    return this.API.get(this.API.getUri()+ "/ip")
  }
}
