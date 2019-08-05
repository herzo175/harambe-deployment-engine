import * as Hapi from "hapi";

const init = async () => {
    const server = new Hapi.Server({
        port: 8080,
        host: "0.0.0.0"
    })

    server.route({
        method: "GET",
        path: "/",
        handler: (request, h) => {
            return 'Hello World!';
        }
    });

    await server.start();
    console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {
    console.log(err);
    process.exit(1);
});

init();
