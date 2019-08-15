import * as config from "config";

// process.env["NODE_CONFIG_DIR"] = __dirname;

class ConfigManager {
    private resolvers : Map<string, (key : string) => string> = new Map();

    public addResolver(name: string, resolver : (key : string) => string) {
        this.resolvers.set(name, resolver);
    }

    public getString(key: string) : string {
        if (key in process.env) {
            return process.env[key];
        } else {
            // NOTE: throws error if not in file config
            const val : string = config.get(key);

            if (val in this.resolvers) {
                return this.resolvers.get(val)(key);
            } else {
                return val;
            }
        }
    }
}

export {
    ConfigManager
}
