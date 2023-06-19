export interface Browser {
    app_code_name: string;
    app_name: string;
    userAgent: string;
}
export interface EventSchemaIn {
    latitude: number;
    longitude: number;
    accuracy?: number;
    ga_user_id?: string;
    window_location_json: WindowLocation;
    browser_json?: Browser;
}
export interface WindowLocation {
    href?: string;
    origin?: string;
    protocol?: string;
    host?: string;
    hostname?: string;
    port?: string;
    pathname?: string;
    search?: string;
    hash?: string;
}
export interface ORJSONModel {
}
