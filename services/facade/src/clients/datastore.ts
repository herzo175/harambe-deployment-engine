import * as mongoose from "mongoose";

// TODO: interface for datastore

class Datastore {
    private client : mongoose.Mongoose;
    private models : Map<mongoose.Schema, mongoose.Model<mongoose.Document, {}>>

    constructor(url: string) {
        this.models = new Map();
        this.client = new mongoose.Mongoose();
        this.client.connect(url, {useNewUrlParser: true});

        this.client.connection.on("error", (err) => {
            console.error("error connecting to datastore:", err);
            throw err;
        });
    }

    public addModel(name: string, schema: mongoose.Schema) {
        this.models.set(schema, this.client.model(name, schema));
    }

    public getModel(schema: mongoose.Schema) : mongoose.Model<mongoose.Document, {}> {
        return this.models.get(schema);
    }
}

export {
    Datastore
}

// const mongoose = require('mongoose');
// mongoose.connect('mongodb://localhost:27017/test', {useNewUrlParser: true});

// const Cat = mongoose.model('Cat', { name: String });

// const kitty = new Cat({ name: 'Zildjian' });
// kitty.save().then(() => console.log('meow'));