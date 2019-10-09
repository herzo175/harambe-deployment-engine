import * as mongoose from "mongoose";
import { ulid } from "ulid";

const Image = new mongoose.Schema(
    {
        "_id": String,
        "jobName": String,
        "dockerfile": String,
        "imageTag": String,
        "directory": String,
        "language": String,
        "buildSteps": {
            type: Array,
            of: String
        },
        "run": String,
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
    Image
}