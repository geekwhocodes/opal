// src/index.ts

import { OpalEvents } from './resources/events';
import { OpalIp } from './resources/ip';


export class Opal {
  events: OpalEvents;
  IP: OpalIp;

  constructor(config: { apiKey: string; baseUrl?: string }) {
    this.events = new OpalEvents(config);
    this.IP = new OpalIp(config)
  }
}
