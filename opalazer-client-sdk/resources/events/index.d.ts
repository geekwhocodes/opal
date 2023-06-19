import { AxiosResponse } from 'axios';
import { Base } from '../base';
import { EventSchemaIn } from './types';
export declare class OpalEvents extends Base {
    create_opal_event(newPost: EventSchemaIn): Promise<AxiosResponse<EventSchemaIn, any>>;
}
