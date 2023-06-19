// src/resources/base.ts

import axios, { AxiosRequestConfig, AxiosInstance } from 'axios';


type Config = {
    apiKey: string;
    baseUrl?: string;
};

abstract class HttpClient {
    protected readonly instance: AxiosInstance;

    public constructor(baseURL: string) {
        this.instance = axios.create({
            baseURL,
        });
    }
}


export abstract class Base {
    private apiKey: string;
    private baseUrl: string;
    protected API: AxiosInstance;

    constructor(config: Config) {
        this.apiKey = config.apiKey;
        this.baseUrl = config.baseUrl || 'https://127.0.0:8000';
        this.API = axios.create({
            baseURL: this.baseUrl,
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json',
                'api-key': this.apiKey,
            }
        })
    }
}
