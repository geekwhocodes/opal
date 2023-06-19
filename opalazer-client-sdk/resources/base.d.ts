import { AxiosInstance } from 'axios';
type Config = {
    apiKey: string;
    baseUrl?: string;
};
export declare abstract class Base {
    private apiKey;
    private baseUrl;
    protected API: AxiosInstance;
    constructor(config: Config);
}
export {};
