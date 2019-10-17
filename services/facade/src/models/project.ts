import * as mongoose from "mongoose";

const Project = new mongoose.Schema(
    {
        "name": String
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
