import * as mongoose from "mongoose";
import { ulid } from "ulid";

const JobRevision = new mongoose.Schema(
    {
        "_id": {
            type: String,
            default: ulid()
        },
        "minInstances": Number,
        "maxInstances": Number,
        "ports": {
            type: Array,
            of: String
        },
        "envVars": {
            type: Map,
            of: String
        },
        "name": String,
        "imageTag": String,
        "project": {
            type: mongoose.Schema.Types.ObjectId,
            ref: "Project"
        }
    },
    {
        timestamps: {
            createdAt: "created",
            updatedAt: "modified"
        }
    }
)

export {
    JobRevision
}