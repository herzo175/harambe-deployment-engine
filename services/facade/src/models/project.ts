import * as mongoose from "mongoose";

const Project = new mongoose.Schema(
    {
        "name": String,
        "language": String // TODO: enum for language (or do not specify)
    },
    {
        timestamps: {
            createdAt: "created",
            updatedAt: "modified"
        }
    }
)

// const Project = mongoose.model("Project", schema);

export {
    Project
}
